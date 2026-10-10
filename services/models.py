from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def string_list(value):
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValidationError('Enter a JSON list of non-empty strings, e.g. ["PLC", "SCADA"].')


phone_validator = RegexValidator(r'^\d{10,15}$', 'Use 10–15 digits, without spaces or a country-code prefix symbol.')
IMAGE_POSITIONS = [('center 35%', 'Upper area'), ('center center', 'Centre'), ('center 65%', 'Lower area')]


class ServicesPage(models.Model):
    # A single CMS record prevents ambiguous selection of the live page.
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    eyebrow = models.CharField(max_length=120)
    heading = models.CharField(max_length=200)
    subheading = models.TextField()
    partner_tags = models.JSONField(default=list, validators=[string_list])
    hero_image = models.ImageField(upload_to='services/hero/', blank=True)
    hero_image_alt = models.CharField(max_length=240, blank=True, help_text='Describe the image for accessibility.')
    hero_image_caption = models.CharField(max_length=180, blank=True)
    hero_image_position = models.CharField(max_length=20, choices=IMAGE_POSITIONS, default='center center')
    contact_name = models.CharField(max_length=120, default='Ashutosh Sonawane')
    contact_role = models.CharField(max_length=120, default='Corporate & Industry Partnerships')
    primary_phone = models.CharField(max_length=15, default='9370432254', validators=[phone_validator])
    secondary_phone = models.CharField(max_length=15, default='9370218408', validators=[phone_validator])
    whatsapp_phone = models.CharField(max_length=15, default='919370432254', validators=[phone_validator])
    location = models.CharField(max_length=200, default='Pimpri-Chinchwad, Maharashtra')
    inquiry_heading = models.CharField(max_length=200, default='Let’s solve your next industrial challenge.')
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Services page'


class OrderedContent(models.Model):
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['order', 'pk']


class Partner(OrderedContent):
    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=180)
    tagline = models.CharField(max_length=180)
    credentials = models.TextField(help_text='Only publish verified credentials or descriptive capabilities.')
    logo = models.ImageField(upload_to='services/partners/', blank=True)

    def __str__(self):
        return self.code


class Service(OrderedContent):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=180)
    short_title = models.CharField(max_length=80)
    audience = models.CharField(max_length=100)
    description = models.TextField()
    outcome = models.CharField(max_length=240)
    specs = models.JSONField(default=list, validators=[string_list])
    deliverables = models.JSONField(default=list, validators=[string_list])
    image = models.ImageField(upload_to='services/capabilities/', blank=True)
    image_alt = models.CharField(max_length=240, blank=True, help_text='Describe the image, without repeating the service title.')
    image_caption = models.CharField(max_length=180, blank=True)
    image_position = models.CharField(max_length=20, choices=IMAGE_POSITIONS, default='center center')

    def __str__(self):
        return self.title


class ValuePillar(OrderedContent):
    ICONS = [(key, key.title()) for key in ['factory', 'wrench', 'users', 'target', 'shield']]
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=20, choices=ICONS)
    metric = models.CharField(max_length=40)
    metric_label = models.CharField(max_length=100)
    commitment = models.CharField(max_length=240, help_text='A delivery commitment; do not claim unverified placement or performance guarantees.')

    def __str__(self):
        return self.title
