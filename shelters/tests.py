from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from shelters.models import ShelterInputModel
from shelters.views import TestSettingsModel


class SheltersViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="shelter", password="secret123")

    def test_get_sets_capacity_from_selected_shelter(self):
        self.client.login(username="shelter", password="secret123")
        response = self.client.get(f"{reverse('shelters')}?shelter=womens")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TestSettingsModel.capacity, TestSettingsModel.womens_regular)

    def test_post_creates_record_and_redirects(self):
        self.client.login(username="shelter", password="secret123")
        payload = {
            "shelter": "mens",
            "regular": 10,
            "respite": 1,
            "guests": 2,
            "hospital": 0,
            "jail": 0,
            "no_show": 0,
            "barred": 0,
            "hold": 0,
        }
        response = self.client.post(reverse("shelters"), payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShelterInputModel.objects.count(), 1)
        self.assertIn("shelter=mens", response.url)