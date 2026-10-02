from django.db import migrations


def remove_promotional_statistics(apps, schema_editor):
    SiteStatistic = apps.get_model("core", "SiteStatistic")
    SiteStatistic.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_companyprofile_google_maps_url"),
    ]

    operations = [
        migrations.RunPython(remove_promotional_statistics, migrations.RunPython.noop),
    ]
