from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("homepage", "0002_alter_pagesection_section_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pagesection",
            name="overview_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
