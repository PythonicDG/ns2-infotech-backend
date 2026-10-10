import hashlib
import json
from django.http import JsonResponse, HttpResponseNotModified
from django.utils.cache import patch_cache_control
from django.views.decorators.http import require_safe
from .models import Partner, Service, ServicesPage, ValuePillar


def image_url(request, field):
    return request.build_absolute_uri(field.url) if field else None


@require_safe
def services_page(request):
    page = ServicesPage.objects.first()
    if not page:
        response = JsonResponse({'detail': 'Services page is not configured.'}, status=503)
        patch_cache_control(response, no_store=True)
        return response
    data = {
        'hero': {'eyebrow': page.eyebrow, 'heading': page.heading, 'subheading': page.subheading,
                 'partner_tags': page.partner_tags, 'image': image_url(request, page.hero_image),
                 'image_alt': page.hero_image_alt, 'image_caption': page.hero_image_caption,
                 'image_position': page.hero_image_position},
        'partners': [{'code': p.code, 'name': p.name, 'tagline': p.tagline, 'credentials': p.credentials,
                      'logo': image_url(request, p.logo)} for p in Partner.objects.filter(is_active=True)],
        'services': [{**{key: getattr(service, key) for key in ['slug', 'title', 'short_title', 'audience', 'description', 'outcome', 'specs', 'deliverables', 'image_alt', 'image_caption', 'image_position']},
                      'image': image_url(request, service.image)} for service in Service.objects.filter(is_active=True)],
        'pillars': list(ValuePillar.objects.filter(is_active=True).values('title', 'description', 'icon', 'metric', 'metric_label', 'commitment')),
        'contact': {key: getattr(page, key) for key in ['contact_name', 'contact_role', 'primary_phone', 'secondary_phone', 'whatsapp_phone', 'location', 'inquiry_heading']},
    }
    etag = '"' + hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest() + '"'
    matches = request.headers.get('If-None-Match', '').split(',')
    response = HttpResponseNotModified() if any(tag.strip().removeprefix('W/') in [etag, '*'] for tag in matches) else JsonResponse(data)
    response['ETag'] = etag
    patch_cache_control(response, public=True, max_age=60, s_maxage=300, stale_while_revalidate=60)
    return response
