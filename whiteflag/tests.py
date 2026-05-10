from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from whiteflag.models import WhiteFlag


class WhiteFlagTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="white", password="secret123")

    def test_create_whiteflag_record_and_redirect_to_edit(self):
        self.client.login(username="white", password="secret123")
        response = self.client.post(reverse("white_flag"), {"men": 2, "women": 1, "children": 1, "non_binary": 0})
        self.assertEqual(response.status_code, 302)
        record = WhiteFlag.objects.get()
        self.assertEqual(record.total, 4)
        self.assertEqual(response.url, reverse("white_flag_edit", kwargs={"pk": record.pk}))

    def test_edit_whiteflag_record_updates_counts(self):
        self.client.login(username="white", password="secret123")
        record = WhiteFlag.objects.create(men=1, women=1, children=0, non_binary=0)
        response = self.client.post(reverse("white_flag_edit", kwargs={"pk": record.pk}), {"men": 3, "women": 1, "children": 1, "non_binary": 1})
        self.assertEqual(response.status_code, 302)
        record.refresh_from_db()
        self.assertEqual(record.total, 6)
