import io
import json
import tempfile
from datetime import timedelta

from PIL import Image
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from announcements.models import Announcement as News, AnnouncementCategory
from core.models import CompanyProfile, ContactMessage, Menu, SubMenu
from homepage.models import PageSection, SectionContent


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class DashboardTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_superuser('editor', 'editor@example.com', 'test-password')
        self.client = Client(enforce_csrf_checks=True)
        self.token = self.client.get('/api/dashboard/session/').json()['csrfToken']

    def sign_in(self, user='editor', password='test-password'):
        response = self.client.post('/api/dashboard/session/', json.dumps({'username': user, 'password': password}),
                                    content_type='application/json', HTTP_X_CSRFTOKEN=self.token)
        if response.status_code == 200:
            self.token = response.json()['csrfToken']
        return response

    def post(self, key, data, pk=None):
        return self.client.post(f'/api/dashboard/content/{key}/' + (f'{pk}/' if pk else ''),
                                data, HTTP_X_CSRFTOKEN=self.token)

    def test_login_and_writes_require_csrf(self):
        response = self.client.post('/api/dashboard/session/', json.dumps({'username': 'editor', 'password': 'test-password'}), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.sign_in().status_code, 200)
        response = self.client.post('/api/dashboard/content/core.menu/', {'text': 'Unsafe'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Menu.objects.exists())

    def test_anonymous_and_nonstaff_are_denied(self):
        self.assertEqual(self.client.get('/api/dashboard/catalog/').status_code, 401)
        get_user_model().objects.create_user('visitor', password='test-password')
        self.assertEqual(self.sign_in('visitor').status_code, 403)
        self.assertEqual(self.client.get('/api/dashboard/catalog/').status_code, 401)

    def test_logout_ends_authenticated_access(self):
        self.sign_in()
        self.assertEqual(self.client.get('/api/dashboard/catalog/').status_code, 200)
        self.assertEqual(self.client.delete('/api/dashboard/session/', HTTP_X_CSRFTOKEN=self.token).status_code, 200)
        self.assertEqual(self.client.get('/api/dashboard/catalog/').status_code, 401)

    def test_model_permissions_and_registry_are_enforced(self):
        staff = get_user_model().objects.create_user('limited', password='test-password', is_staff=True)
        staff.user_permissions.add(Permission.objects.get(codename='view_menu', content_type__app_label='core'))
        self.sign_in('limited')
        resources = [resource['key'] for group in self.client.get('/api/dashboard/catalog/').json()['groups'] for resource in group['resources']]
        self.assertEqual(resources, ['core.menu'])
        self.assertEqual(self.post('core.menu', {'text': 'Forbidden'}).status_code, 403)
        self.assertEqual(self.client.get('/api/dashboard/content/auth.user/').status_code, 404)
        self.assertEqual(self.client.get('/api/dashboard/content/core.contactmessage/').status_code, 403)

    def test_create_edit_validation_public_output_and_audit(self):
        self.sign_in()
        self.assertEqual(self.post('core.menu', {'text': ''}).status_code, 400)
        created = self.post('core.menu', {'text': 'Training', 'url': '/modules', 'order': 2, 'is_active': 'true'})
        self.assertEqual(created.status_code, 201, created.content)
        pk = created.json()['record']['id']
        self.assertEqual(self.post('core.menu', {'text': 'Updated training', 'url': '/modules', 'order': 1, 'is_active': 'true'}, pk).status_code, 200)
        public = self.client.get('/api/core/header-footer/').json()
        self.assertEqual(public['header']['menu'][0]['text'], 'Updated training')
        self.assertEqual(LogEntry.objects.filter(user=self.user).count(), 2)
        self.post('core.menu', {'text': 'Hidden', 'order': 0, 'is_active': 'false'}, pk)
        self.assertEqual(self.client.get('/api/core/header-footer/').json()['header']['menu'], [])

    def test_homepage_parent_is_assigned_without_internal_fields(self):
        self.sign_in()
        CompanyProfile.objects.create(name='MIA', description='Training')
        response = self.post('homepage.pagesection', {'section_type': 'FAQ', 'heading': 'Questions', 'order': 0, 'is_active': 'true'})
        self.assertEqual(response.status_code, 201, response.content)
        section = PageSection.objects.get()
        self.assertIsInstance(section.content_object, CompanyProfile)
        fields = self.client.get('/api/dashboard/content/homepage.pagesection/').json()['fields']
        self.assertNotIn('content_type', [field['name'] for field in fields])
        self.post('homepage.sectioncontent', {'section': section.pk, 'question': 'How to enrol?', 'answer': 'Contact us.', 'order': 0, 'is_active': 'true'})
        visible = self.client.get('/api/homepage/fetch-homepage/').json()
        self.assertEqual(visible[0]['content_items'][0]['answer'], 'Contact us.')

    def test_parent_filter_search_and_pagination(self):
        self.sign_in()
        first = Menu.objects.create(text='A')
        second = Menu.objects.create(text='B')
        SubMenu.objects.create(menu=first, text='First', url='/first', slug='first')
        SubMenu.objects.create(menu=second, text='Second', url='/second', slug='second')
        data = self.client.get(f'/api/dashboard/content/core.submenu/?menu={first.pk}').json()
        self.assertEqual([item['values']['text'] for item in data['records']], ['First'])
        for index in range(35):
            Menu.objects.create(text=f'Course {index}')
        data = self.client.get('/api/dashboard/content/core.menu/?search=Course&page=2').json()
        self.assertEqual(data['count'], 35)
        self.assertEqual(len(data['records']), 5)

    def test_delete_previews_cascade_before_confirmation(self):
        self.sign_in()
        menu = Menu.objects.create(text='Parent')
        SubMenu.objects.create(menu=menu, text='Child', url='/child')
        url = f'/api/dashboard/content/core.menu/{menu.pk}/'
        response = self.client.delete(url, HTTP_X_CSRFTOKEN=self.token)
        self.assertEqual(response.json()['relatedCount'], 1)
        self.assertTrue(Menu.objects.filter(pk=menu.pk).exists())
        self.assertEqual(self.client.delete(url + '?confirm=yes', HTTP_X_CSRFTOKEN=self.token).status_code, 200)
        self.assertFalse(SubMenu.objects.exists())

    def test_enquiries_are_read_only_even_for_superusers(self):
        self.sign_in()
        message = ContactMessage.objects.create(full_name='Student', email_address='student@example.com', subject='general', message='Course details please')
        self.assertEqual(self.client.get('/api/dashboard/content/core.contactmessage/').status_code, 200)
        self.assertEqual(self.post('core.contactmessage', {'message': 'Changed'}, message.pk).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/dashboard/content/core.contactmessage/{message.pk}/', HTTP_X_CSRFTOKEN=self.token).status_code, 403)

    def test_announcement_drafts_schedule_categories_and_sanitization(self):
        self.sign_in()
        category = AnnouncementCategory.objects.create(name='News')
        data = {'title': 'New batch', 'category': category.pk, 'short_description': 'Registration open',
                'full_description': '<strong>Welcome</strong><img src=x onerror=alert(1)><a href="javascript:alert(1)">link</a>',
                'publish_date': timezone.localdate().isoformat(), 'is_active': 'false'}
        response = self.post('announcements.announcement', data)
        self.assertEqual(response.status_code, 201, response.content)
        pk = response.json()['record']['id']
        self.assertEqual(self.client.get('/api/announcements/items/').json(), [])
        data['is_active'] = 'true'
        self.post('announcements.announcement', data, pk)
        public = self.client.get('/api/announcements/items/').json()
        self.assertEqual(len(public), 1)
        self.assertIn('<strong>Welcome</strong>', public[0]['full_description'])
        self.assertNotIn('onerror', public[0]['full_description'])
        self.assertNotIn('javascript:', public[0]['full_description'])
        News.objects.filter(pk=pk).update(publish_date=timezone.localdate() + timedelta(days=1))
        self.assertEqual(self.client.get('/api/announcements/items/').json(), [])
        self.assertEqual(self.client.get('/api/announcements/items/new-batch/').status_code, 404)
        News.objects.filter(pk=pk).update(publish_date=timezone.localdate())
        category.is_active = False
        category.save()
        self.assertEqual(self.client.get('/api/announcements/items/').json(), [])

    def test_image_upload_preserve_clear_and_invalid_file(self):
        self.sign_in()
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            content = io.BytesIO()
            Image.new('RGB', (16, 16), 'red').save(content, format='PNG')
            response = self.post('core.companyprofile', {'name': 'MIA', 'description': 'Training', 'is_active': 'true',
                'logo': SimpleUploadedFile('logo.png', content.getvalue(), content_type='image/png')})
            self.assertEqual(response.status_code, 201, response.content)
            company = CompanyProfile.objects.get()
            original = company.logo.name
            self.assertTrue(original.endswith('.webp'))
            self.post('core.companyprofile', {'name': 'MIA updated', 'description': 'Training', 'is_active': 'true'}, company.pk)
            company.refresh_from_db()
            self.assertEqual(company.logo.name, original)
            self.post('core.companyprofile', {'name': 'MIA', 'description': 'Training', 'logo-clear': 'true', 'is_active': 'true'}, company.pk)
            company.refresh_from_db()
            self.assertFalse(company.logo)
            response = self.post('core.companyprofile', {'name': 'MIA', 'description': 'Training',
                'logo': SimpleUploadedFile('fake.png', b'not an image', content_type='image/png')}, company.pk)
            self.assertEqual(response.status_code, 400)
            response = self.post('core.companyprofile', {'name': 'MIA', 'description': 'Training',
                'logo': SimpleUploadedFile('script.html', b'<script>bad</script>')}, company.pk)
            self.assertEqual(response.status_code, 400)

    def test_optional_page_copy_is_public_and_singleton(self):
        self.assertEqual(self.client.get('/api/page-copy/contact/').json(), {'contact_info': {}})
        self.sign_in()
        response = self.post('core.contactpage', {'heading': 'Visit our campus'})
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(self.client.get('/api/page-copy/contact/').json()['heading'], 'Visit our campus')
        self.assertEqual(self.post('core.contactpage', {'heading': 'Duplicate'}).status_code, 409)

    def test_login_rate_limit(self):
        for _ in range(10):
            self.assertEqual(self.sign_in(password='wrong').status_code, 403)
        self.assertEqual(self.sign_in(password='wrong').status_code, 429)

    def test_all_collections_have_usable_editor_metadata(self):
        self.sign_in()
        groups = self.client.get('/api/dashboard/catalog/').json()['groups']
        for group in groups:
            for resource in group['resources']:
                response = self.client.get(f"/api/dashboard/content/{resource['key']}/")
                self.assertEqual(response.status_code, 200, response.content)
                self.assertIsInstance(response.json()['fields'], list)

    def test_unsafe_links_are_rejected(self):
        self.sign_in()
        response = self.post('core.menu', {'text': 'Unsafe', 'url': 'javascript:alert(1)'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('url', response.json()['errors'])
        self.assertFalse(Menu.objects.exists())

    def test_hidden_about_and_course_items_stay_off_public_responses(self):
        from aboutus.models import PageSection as AboutSection, SectionContent as AboutContent
        from aboutus.serializers import PageSectionSerializer as AboutSerializer
        from modules.models import PageSection as CourseSection, SectionContent as CourseContent
        from modules.serializers import PageSectionSerializer as CourseSerializer
        for section_model, content_model, serializer in [
            (AboutSection, AboutContent, AboutSerializer), (CourseSection, CourseContent, CourseSerializer),
        ]:
            section = section_model.objects.create(section_type='HERO')
            content_model.objects.create(section=section, title='Visible')
            content_model.objects.create(section=section, title='Draft', is_active=False)
            self.assertEqual([item['title'] for item in serializer(section).data['content_items']], ['Visible'])

    def test_every_section_type_has_valid_field_rules(self):
        from django.apps import apps
        from .dashboard_fields import SECTION_FIELDS, ITEM_FIELDS
        for app in ('homepage', 'aboutus', 'modules'):
            section = apps.get_model(app, 'PageSection')
            item = apps.get_model(app, 'SectionContent')
            expected = {value for value, _ in section.SECTION_TYPES}
            self.assertEqual(set(SECTION_FIELDS[app]), expected)
            self.assertEqual(set(ITEM_FIELDS[app]), expected)
            for model, rules in ((section, SECTION_FIELDS[app]), (item, ITEM_FIELDS[app])):
                actual = {field.name for field in model._meta.fields}
                for names in rules.values():
                    self.assertFalse(names - actual)

    def test_gallery_and_faq_metadata_matches_relevant_fields(self):
        from aboutus.models import PageSection as AboutSection
        self.sign_in()
        gallery = AboutSection.objects.create(section_type='GALLERY')
        data = self.client.get('/api/dashboard/content/aboutus.sectioncontent/').json()
        option = next(option for field in data['fields'] if field['name'] == 'section' for option in field['options'] if option['value'] == gallery.pk)
        self.assertEqual(option['sectionType'], 'GALLERY')
        visible = {field['name'] for field in data['fields'] if field['visibleFor'] is None or 'GALLERY' in field['visibleFor']}
        self.assertEqual(visible, {'section', 'order', 'is_active', 'image', 'label'})
        gallery_caption = next(field for field in data['fields'] if field['name'] == 'label')
        self.assertEqual(gallery_caption['labelsFor']['GALLERY'], 'Image caption')
        data = self.client.get('/api/dashboard/content/homepage.sectioncontent/').json()
        visible = {field['name'] for field in data['fields'] if field['visibleFor'] is None or 'FAQ' in field['visibleFor']}
        self.assertEqual(visible, {'section', 'order', 'is_active', 'question', 'answer'})

    def test_simplified_gallery_save_preserves_hidden_values_and_images(self):
        from aboutus.models import PageSection as AboutSection, SectionContent as AboutContent
        self.sign_in()
        gallery = AboutSection.objects.create(section_type='GALLERY', background_image='legacy/background.webp')
        item = AboutContent.objects.create(section=gallery, label='Old caption', title='Legacy title', description='Keep this', person_name='Legacy name', image='legacy/photo.webp')
        response = self.post('aboutus.sectioncontent', {'section': gallery.pk, 'label': 'New caption', 'order': 3, 'is_active': 'true', 'person_name': 'Should be ignored'}, item.pk)
        self.assertEqual(response.status_code, 200, response.content)
        item.refresh_from_db()
        self.assertEqual((item.label, item.order), ('New caption', 3))
        self.assertEqual((item.title, item.description, item.person_name, item.image.name), ('Legacy title', 'Keep this', 'Legacy name', 'legacy/photo.webp'))
        response = self.post('aboutus.pagesection', {'section_type': 'GALLERY', 'heading': 'Our gallery', 'order': 1, 'is_active': 'true'}, gallery.pk)
        self.assertEqual(response.status_code, 200, response.content)
        gallery.refresh_from_db()
        self.assertEqual(gallery.background_image.name, 'legacy/background.webp')

    def test_changing_item_parent_uses_new_section_fields(self):
        from aboutus.models import PageSection as AboutSection, SectionContent as AboutContent
        self.sign_in()
        gallery = AboutSection.objects.create(section_type='GALLERY')
        team = AboutSection.objects.create(section_type='OUR_TEAM')
        item = AboutContent.objects.create(section=gallery, label='Photo', question='Legacy question')
        response = self.post('aboutus.sectioncontent', {'section': team.pk, 'person_name': 'New mentor', 'person_role': 'Trainer', 'label': 'New mentor', 'order': 0, 'is_active': 'true'}, item.pk)
        self.assertEqual(response.status_code, 200, response.content)
        item.refresh_from_db()
        self.assertEqual(item.section_id, team.pk)
        self.assertEqual(item.person_name, 'New mentor')
        self.assertEqual(item.question, 'Legacy question')

    def test_new_faq_and_invalid_parent_validate_with_simplified_forms(self):
        from aboutus.models import PageSection as AboutSection
        self.sign_in()
        CompanyProfile.objects.create(name='MIA', description='Training')
        response = self.post('homepage.pagesection', {'section_type': 'FAQ', 'heading': 'Questions', 'is_active': 'true', 'order': 0})
        self.assertEqual(response.status_code, 201, response.content)
        section_id = response.json()['record']['id']
        response = self.post('homepage.sectioncontent', {'section': section_id, 'question': 'Course timings?', 'answer': 'Ask our advisors.', 'is_active': 'true', 'order': 0})
        self.assertEqual(response.status_code, 201, response.content)
        response = self.post('aboutus.sectioncontent', {'section': 'invalid', 'order': 0})
        self.assertEqual(response.status_code, 400)
        self.assertIn('section', response.json()['errors'])
