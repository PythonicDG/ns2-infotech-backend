from django.core.files.storage import default_storage
from django.db import migrations


def seed_photography(apps, schema_editor):
    """Reuse the project's existing media, preserving images selected by editors."""
    Page = apps.get_model('services', 'ServicesPage')
    Service = apps.get_model('services', 'Service')
    page = Page.objects.first()
    hero_path = 'sections/WhatsApp_Image_2026-06-25_at_5.25.44_PM.webp'
    if page and not page.hero_image and default_storage.exists(hero_path):
        page.hero_image = hero_path
        page.hero_image_alt = 'A group working together at an automation training workstation at MIA'
        page.hero_image_caption = 'Practical learning. Real equipment. Connected expertise.'
        page.hero_image_position = 'center 35%'
        page.save()

    images = {
        'corporate-training': (
            'section_content/WhatsApp_Image_2026-06-25_at_5.25.42_PM_1.webp',
            'Two people working on PLC programming beside an industrial training panel',
            'Hands-on learning with industrial control systems', 'center center'),
        'automation-services': (
            'icons/IMG_9731.JPG.webp',
            'Siemens PLC, HMI and wired controls on a MIA automation training panel',
            'PLC, HMI and control systems in practice', 'center 65%'),
        'industry-ready-employees': (
            'sections/WhatsApp_Image_2026-06-25_at_5.25.43_PM.webp',
            'A participant taking notes beside a laptop during a technical learning session',
            'Technical preparation for the next industry opportunity', 'center 35%'),
        'training-placement': (
            'icons/IMG_9728.JPG.webp',
            'MIA process automation training equipment with tanks, controls and wiring',
            'Build practical skills on application-based training equipment', 'center 65%'),
    }
    for slug, (path, alt, caption, position) in images.items():
        if default_storage.exists(path):
            Service.objects.filter(slug=slug, image='').update(
                image=path, image_alt=alt, image_caption=caption, image_position=position)


class Migration(migrations.Migration):
    dependencies = [('services', '0004_service_image_service_image_alt_and_more')]
    operations = [migrations.RunPython(seed_photography, migrations.RunPython.noop)]
