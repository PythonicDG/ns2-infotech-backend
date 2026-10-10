from django.db import migrations


class Migration(migrations.Migration):
    # Existing installations have a legacy services.0001_initial marker and
    # PageSection tables, although the former app is absent from this checkout.
    # Keep that marker and leave those tables untouched. Our new schema is an
    # additive 0002 migration, supporting both existing and clean databases.
    initial = True
    dependencies = []
    operations = []
