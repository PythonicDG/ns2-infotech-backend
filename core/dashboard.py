"""Private, form-validated CMS API. Public website endpoints remain unchanged."""
import json
from functools import wraps
from urllib.parse import urlsplit

from django import forms
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.db.models import Q
from django.db.models.deletion import Collector, ProtectedError, RestrictedError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .dashboard_fields import policy, editable_fields, ITEM_FIELDS, ITEM_LABELS


# Explicit allowlist: authentication, sessions and other internal models cannot be edited.
GROUPS = [
    ('home', 'Home page', '/', [
        ('homepage.PageSection', 'Page sections'), ('homepage.SectionContent', 'Section items'),
        ('core.SiteStatistic', 'Credibility statistics'), ('core.Announcement', 'Header notices')]),
    ('about', 'About us', '/aboutus', [
        ('aboutus.PageSection', 'Page sections'), ('aboutus.SectionContent', 'Section items & team')]),
    ('modules', 'Courses & modules', '/modules', [
        ('modules.Module', 'Courses'), ('modules.PageSection', 'Page & course sections'),
        ('modules.SectionContent', 'Section items')]),
    ('services', 'Services', '/services', [
        ('services.ServicesPage', 'Page & contact details'), ('services.Partner', 'Partners'),
        ('services.Service', 'Services'), ('services.ValuePillar', 'Value pillars')]),
    ('announcements', 'Announcements', '/announcements', [
        ('announcements.Announcement', 'Announcements'), ('announcements.AnnouncementCategory', 'Categories'),
        ('announcements.AnnouncementPage', 'Page text & banner')]),
    ('contact', 'Contact page', '/contact', [
        ('core.ContactPage', 'Page text & banner'), ('core.ContactInfo', 'Contact information'),
        ('homepage.PageSection', 'Shared contact & FAQ sections'), ('homepage.SectionContent', 'Shared section items')]),
    ('site', 'Website settings', '/', [
        ('core.CompanyProfile', 'Company, logo & footer contact'), ('core.Menu', 'Navigation links'),
        ('core.SubMenu', 'Dropdown links'), ('core.FooterSection', 'Footer groups'),
        ('core.FooterItem', 'Footer links'), ('core.FooterSubscription', 'Subscription labels'),
        ('core.SocialLink', 'Social links')]),
    ('inbox', 'Enquiry inbox', '/contact', [('core.ContactMessage', 'Messages')]),
]
REGISTRY = {label.lower(): (apps.get_model(label), title)
            for _, _, _, resources in GROUPS for label, title in resources}
HIDDEN = {'content_type', 'object_id'}
MAX_UPLOAD = 10 * 1024 * 1024


def reply(data, status=200):
    return JsonResponse(data, status=status)


def staff_only(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reply({'detail': 'Please sign in to continue.'}, 401)
        if not request.user.is_active or not request.user.is_staff:
            return reply({'detail': 'A staff account is required.'}, 403)
        return view(request, *args, **kwargs)
    return wrapped


def allowed(user, model, action):
    if model._meta.label_lower == 'core.contactmessage' and action != 'view':
        return False
    return user.has_perm(f'{model._meta.app_label}.{action}_{model._meta.model_name}')


def permissions(user, model):
    perms = {action: allowed(user, model, action) for action in ('view', 'add', 'change', 'delete')}
    if model._meta.label_lower in {'services.servicespage', 'core.contactpage', 'announcements.announcementpage'} and model.objects.exists():
        perms['add'] = False
    return perms


@never_cache
@csrf_protect
@require_http_methods(['GET', 'POST', 'DELETE'])
def session(request):
    if request.method == 'DELETE':
        logout(request)
    elif request.method == 'POST':
        # Bound attempts per source address; shared cache is recommended for multi-worker deployments.
        key = 'dashboard-login:' + request.META.get('REMOTE_ADDR', '')
        if cache.get(key, 0) >= 10:
            return reply({'detail': 'Too many sign-in attempts. Try again in 15 minutes.'}, 429)
        try:
            data = json.loads(request.body)
        except (ValueError, UnicodeDecodeError):
            return reply({'detail': 'Invalid sign-in request.'}, 400)
        if not isinstance(data, dict):
            return reply({'detail': 'Invalid sign-in request.'}, 400)
        username, password = data.get('username'), data.get('password')
        if not isinstance(username, str) or not isinstance(password, str):
            return reply({'detail': 'Enter your username and password.'}, 400)
        user = authenticate(request, username=username, password=password)
        if not user or not user.is_active or not user.is_staff:
            cache.set(key, cache.get(key, 0) + 1, 900)
            return reply({'detail': 'Invalid credentials or this account does not have staff access.'}, 403)
        cache.delete(key)
        login(request, user)
    user = request.user
    return reply({'csrfToken': get_token(request), 'user': {
        'username': user.get_username(), 'name': user.get_full_name() or user.get_username(),
    } if user.is_authenticated and user.is_active and user.is_staff else None})


@never_cache
@require_http_methods(['GET'])
@staff_only
def catalog(request):
    groups = []
    for key, title, url, resources in GROUPS:
        entries = []
        for label, name in resources:
            model = REGISTRY[label.lower()][0]
            perms = permissions(request.user, model)
            if perms['view']:
                entries.append({'key': label.lower(), 'title': name,
                                'count': model.objects.count(), 'permissions': perms})
        if entries:
            groups.append({'key': key, 'title': title, 'url': url, 'resources': entries})
    return reply({'groups': groups})


def form_class(model, data=None, obj=None):
    fields = editable_fields(model, data, obj) if data is not None else [f.name for f in model._meta.fields if f.editable and not f.primary_key and f.name not in HIDDEN]
    return forms.modelform_factory(model, fields=fields)


def schema(model):
    output = []
    rules, common = policy(model)
    for name, field in form_class(model)().fields.items():
        db_field = model._meta.get_field(name)
        kind = 'text'
        options = []
        if isinstance(field, forms.ModelChoiceField):
            kind = 'relation'
            # Labels are available only for allowlisted content relationships.
            options = [{'value': obj.pk, 'label': str(obj),
                        **({'sectionType': obj.section_type} if hasattr(obj, 'section_type') else {})}
                       for obj in field.queryset]
        elif hasattr(field, 'choices') and field.choices:
            kind = 'select'
            options = [{'value': value, 'label': str(label),
                        **({'supportsItems': bool(ITEM_FIELDS[model._meta.app_label].get(value))}
                           if name == 'section_type' and model._meta.app_label in ITEM_FIELDS else {})}
                       for value, label in field.choices if value != '']
        elif isinstance(db_field, models.BooleanField):
            kind = 'boolean'
        elif isinstance(db_field, models.ImageField):
            kind = 'image'
        elif isinstance(db_field, models.FileField):
            kind = 'file'
        elif isinstance(db_field, models.JSONField):
            kind = 'list'
        elif isinstance(db_field, models.TextField):
            kind = 'textarea'
        elif isinstance(db_field, models.DateTimeField):
            kind = 'datetime-local'
        elif isinstance(db_field, models.DateField):
            kind = 'date'
        elif isinstance(db_field, models.IntegerField):
            kind = 'number'
        elif isinstance(db_field, models.EmailField):
            kind = 'email'
        initial = field.initial() if callable(field.initial) else field.initial
        if hasattr(initial, 'isoformat'):
            initial = initial.isoformat()[:10] if kind == 'date' else initial.isoformat()
        output.append({'name': name, 'label': 'Visible on website' if name == 'is_active' else str(field.label).capitalize(),
                       'type': kind, 'required': field.required, 'help': str(field.help_text),
                       'maxLength': field.max_length if hasattr(field, 'max_length') else None,
                       'options': options, 'default': initial,
                       'visibleFor': [key for key, names in rules.items() if name in names] if rules is not None and name not in common else None,
                       'labelsFor': {key: labels[name] for key, labels in ITEM_LABELS.get(model._meta.app_label, {}).items() if name in labels}
                           if model._meta.model_name == 'sectioncontent' else {},
                       'relation': db_field.related_model._meta.label_lower if kind == 'relation' else None})
    return output


def record(obj, request):
    values = {}
    for field in obj._meta.fields:
        if field.name in HIDDEN:
            continue
        value = getattr(obj, field.attname)
        if isinstance(field, models.FileField):
            value = value.url if value else None
        values[field.name] = value
    return {'id': obj.pk, 'label': str(obj), 'values': values}


def audit(request, obj, flag):
    LogEntry.objects.log_actions(user_id=request.user.pk, queryset=[obj], action_flag=flag,
                                 change_message='Updated through website dashboard', single_object=True)


@never_cache
@csrf_protect
@require_http_methods(['GET', 'POST', 'DELETE'])
@staff_only
def resource(request, key, pk=None):
    entry = REGISTRY.get(key)
    if not entry:
        return reply({'detail': 'Unknown content collection.'}, 404)
    model, title = entry
    action = 'view' if request.method == 'GET' else 'delete' if request.method == 'DELETE' else 'change' if pk else 'add'
    if not allowed(request.user, model, action):
        return reply({'detail': 'Your account does not have permission for this action.'}, 403)
    obj = get_object_or_404(model, pk=pk) if pk else None
    if request.method == 'GET':
        if obj:
            return reply({'record': record(obj, request), 'fields': schema(model), 'permissions': permissions(request.user, model)})
        queryset = model.objects.all()
        if 'section_type' in request.GET and hasattr(model, 'SECTION_TYPES'):
            section_type = request.GET['section_type']
            if section_type not in dict(model.SECTION_TYPES):
                return reply({'detail': 'Invalid section type.'}, 400)
            queryset = queryset.filter(section_type=section_type)
        # Only explicit foreign keys can be used to navigate child content.
        for field in model._meta.fields:
            if isinstance(field, models.ForeignKey) and field.name not in HIDDEN and field.name in request.GET:
                value = request.GET[field.name]
                if value == 'none' and field.null:
                    queryset = queryset.filter(**{field.name + '__isnull': True})
                elif value.isdigit():
                    queryset = queryset.filter(**{field.attname: int(value)})
                else:
                    return reply({'detail': 'Invalid parent filter.'}, 400)
        search = request.GET.get('search', '').strip()[:200]
        if search:
            query = Q()
            for field in model._meta.fields:
                if isinstance(field, (models.CharField, models.TextField)):
                    query |= Q(**{field.name + '__icontains': search})
            queryset = queryset.filter(query)
        try:
            page = max(1, int(request.GET.get('page', 1)))
        except ValueError:
            return reply({'detail': 'Invalid page number.'}, 400)
        queryset = queryset.order_by(*(list(model._meta.ordering or []) + ['pk']))
        count = queryset.count()
        return reply({'title': title, 'fields': schema(model), 'permissions': permissions(request.user, model),
                      'count': count, 'page': page, 'records': [record(item, request) for item in queryset[(page-1)*30:page*30]]})
    if request.method == 'DELETE':
        if obj is None:
            return reply({'detail': 'Choose a record to delete.'}, 400)
        try:
            collector = Collector(using='default')
            collector.collect([obj])
            dependents = sum(len(items) for items in collector.data.values()) - 1
            dependents += sum(qs.count() for qs in collector.fast_deletes)
            if request.GET.get('confirm') != 'yes':
                return reply({'label': str(obj), 'relatedCount': dependents, 'confirmationRequired': True})
            with transaction.atomic():
                audit(request, obj, DELETION)
                obj.delete()
        except (ProtectedError, RestrictedError):
            return reply({'detail': 'This record is used by other content and cannot be deleted.'}, 409)
        return reply({'deleted': True})
    data = request.POST.copy()
    for field in model._meta.fields:
        if isinstance(field, models.FileField) and data.get(field.name + '-clear') == 'true':
            data[field.name + '-clear'] = 'on'
    for upload in request.FILES.values():
        if upload.size > MAX_UPLOAD:
            return reply({'detail': 'Files must be smaller than 10 MB.'}, 400)
        extension = upload.name.rsplit('.', 1)[-1].lower()
        if extension not in {'jpg', 'jpeg', 'png', 'webp', 'gif', 'pdf', 'doc', 'docx'}:
            return reply({'detail': 'Use JPG, PNG, WebP, GIF, PDF, DOC or DOCX files.'}, 400)
    if model._meta.label_lower in {'services.servicespage', 'core.contactpage', 'announcements.announcementpage'} and obj is None and model.objects.exists():
        return reply({'detail': 'This page configuration already exists. Edit it instead.'}, 409)
    instance = obj or model()
    if model._meta.label_lower == 'homepage.pagesection' and obj is None:
        company = apps.get_model('core.CompanyProfile').objects.first()
        if not company:
            return reply({'detail': 'Add company information in Website settings first.'}, 400)
        instance.content_object = company
    # Slugs are generated for new records but remain editable for deliberate URL changes.
    if hasattr(instance, 'slug') and not data.get('slug'):
        data['slug'] = slugify(data.get('title') or data.get('name') or data.get('text') or '')
    selected_form = form_class(model, data, obj)
    unsafe_links = {}
    for name in selected_form.base_fields:
        if name == 'url' or name.endswith('_url') or name == 'social_link':
            try:
                scheme = urlsplit(data.get(name, '').strip()).scheme.lower()
                if scheme not in {'', 'http', 'https', 'mailto', 'tel'}:
                    raise ValueError('Unsupported link scheme')
            except ValueError:
                unsafe_links[name] = [{'message': 'Use a website address, relative page path, email or telephone link.', 'code': 'invalid'}]
    if unsafe_links:
        return reply({'detail': 'Please check the highlighted links.', 'errors': unsafe_links}, 400)
    form = selected_form(data=data, files=request.FILES, instance=instance)
    if not form.is_valid():
        return reply({'detail': 'Please check the highlighted fields.', 'errors': form.errors.get_json_data()}, 400)
    try:
        with transaction.atomic():
            saved = form.save()
            audit(request, saved, CHANGE if obj else ADDITION)
    except (IntegrityError, ValidationError):
        return reply({'detail': 'This conflicts with existing content. Check unique names and page URLs.'}, 409)
    return reply({'record': record(saved, request)}, 200 if obj else 201)


@never_cache
@require_http_methods(['GET'])
def page_copy(request, page):
    label = {'contact': 'core.ContactPage', 'announcements': 'announcements.AnnouncementPage'}.get(page)
    if not label:
        return reply({'detail': 'Unknown page.'}, 404)
    obj = apps.get_model(label).objects.first()
    data = record(obj, request)['values'] if obj else {}
    if page == 'contact':
        info = apps.get_model('core.ContactInfo').objects.first()
        data['contact_info'] = record(info, request)['values'] if info and data.get('use_contact_information') else {}
    return reply(data)
