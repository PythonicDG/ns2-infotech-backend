from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Partner, Service, ServicesPage, ValuePillar, string_list


class ServicesApiTests(TestCase):
    def test_seeded_content_and_cache(self):
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['partners']), 3)
        self.assertEqual(len(data['services']), 4)
        self.assertEqual(len(data['pillars']), 5)
        self.assertEqual(data['contact']['primary_phone'], '9370432254')
        self.assertIn('public', response['Cache-Control'])
        self.assertIn('s-maxage=300', response['Cache-Control'])
        cached = self.client.get('/api/services/', HTTP_IF_NONE_MATCH=response['ETag'])
        self.assertEqual(cached.status_code, 304)

    def test_active_filter_order_and_etag_updates(self):
        before = self.client.get('/api/services/')['ETag']
        item = Service.objects.first()
        item.is_active = False
        item.save()
        response = self.client.get('/api/services/')
        self.assertEqual(len(response.json()['services']), 3)
        self.assertNotEqual(response['ETag'], before)
        Partner.objects.update(is_active=False)
        ValuePillar.objects.update(is_active=False)
        response = self.client.get('/api/services/')
        self.assertEqual(response.json()['partners'], [])
        self.assertEqual(response.json()['pillars'], [])

    def test_image_urls_are_absolute(self):
        page = ServicesPage.objects.first()
        page.hero_image = 'services/hero/factory.jpg'
        page.save()
        partner = Partner.objects.first()
        partner.logo = 'services/partners/aes.png'
        partner.save()
        service = Service.objects.first()
        service.image = 'services/capabilities/training.webp'
        service.image_alt = 'Training panel'
        service.image_caption = 'Practical training'
        service.image_position = 'center 35%'
        service.save()
        data = self.client.get('/api/services/', secure=True).json()
        self.assertEqual(data['hero']['image'], 'https://testserver/media/services/hero/factory.jpg')
        self.assertEqual(data['partners'][0]['logo'], 'https://testserver/media/services/partners/aes.png')
        self.assertEqual(data['services'][0]['image'], 'https://testserver/media/services/capabilities/training.webp')
        self.assertEqual(data['services'][0]['image_alt'], 'Training panel')
        self.assertEqual(data['services'][0]['image_caption'], 'Practical training')
        self.assertEqual(data['services'][0]['image_position'], 'center 35%')

    def test_editor_can_replace_and_clear_images(self):
        service = Service.objects.first()
        before = self.client.get('/api/services/')['ETag']
        service.image = 'services/capabilities/new-photo.webp'
        service.save()
        response = self.client.get('/api/services/')
        self.assertNotEqual(response['ETag'], before)
        self.assertTrue(response.json()['services'][0]['image'].endswith('/new-photo.webp'))
        service.image = ''
        service.save()
        page = ServicesPage.objects.first()
        page.hero_image = ''
        page.save()
        data = self.client.get('/api/services/').json()
        self.assertIsNone(data['services'][0]['image'])
        self.assertIsNone(data['hero']['image'])

    def test_empty_cms_is_not_cached(self):
        ServicesPage.objects.all().delete()
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Cache-Control'], 'no-store')

    def test_read_only_endpoint(self):
        self.assertEqual(self.client.post('/api/services/', {}).status_code, 405)

    def test_list_validation(self):
        string_list(['PLC', 'SCADA'])
        for value in ['PLC', {'PLC': True}, [''], [1]]:
            with self.assertRaises(ValidationError):
                string_list(value)
