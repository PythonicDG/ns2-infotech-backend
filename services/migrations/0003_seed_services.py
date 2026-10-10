import json
from pathlib import Path
from django.db import migrations


def seed(apps, schema_editor):
    data = json.loads((Path(__file__).resolve().parent.parent / 'initial_content.json').read_text(encoding='utf-8'))
    Page = apps.get_model('services', 'ServicesPage')
    Page.objects.get_or_create(pk=1, defaults={
        'eyebrow': data['hero']['eyebrow'], 'heading': data['hero']['heading'],
        'subheading': data['hero']['subheading'], 'partner_tags': data['hero']['partner_tags'],
        **data['contact'],
    })
    for model_name, key, identity in [('Partner', 'partners', 'code'), ('Service', 'services', 'slug'), ('ValuePillar', 'pillars', 'title')]:
        Model = apps.get_model('services', model_name)
        for index, item in enumerate(data[key]):
            fields = {k: v for k, v in item.items() if k != 'logo'}
            value = fields.pop(identity)
            Model.objects.get_or_create(**{identity: value}, defaults={**fields, 'order': index})


class Migration(migrations.Migration):
    dependencies = [('services', '0002_alliance_schema')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
