from django.test import Client, TestCase

from .models import Queue, User


class SecurityRegressionTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create(
            spotify_id="spotify-user-1",
            display_name="Test User",
            access_token="access-token",
            refresh_token="refresh-token",
        )
        self.queue = Queue.objects.create(
            user=self.user,
            name="Regression Queue",
        )
        session = self.client.session
        session["user_id"] = self.user.id
        session.save()

    def test_csrf_endpoint_issues_token(self):
        response = self.client.get("/csrf/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfToken", response.json())
        self.assertIn("csrftoken", response.cookies)

    def test_queue_delete_rejects_missing_csrf_token(self):
        response = self.client.delete(f"/queue/{self.queue.id}/delete/")

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Queue.objects.filter(id=self.queue.id).exists())

    def test_restore_queue_is_not_triggered_by_get(self):
        response = self.client.get(f"/queue/{self.queue.id}/restore/")

        self.assertEqual(response.status_code, 405)
