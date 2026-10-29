from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Post


class PostAccessTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='geheim123')
        self.draft = Post.objects.create(author=self.user, title='Entwurf', text='noch geheim')

    def test_visitor_cannot_see_draft(self):
        response = self.client.get(f'/post/{self.draft.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_author_can_see_draft(self):
        self.client.login(username='tester', password='geheim123')
        response = self.client.get(f'/post/{self.draft.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_publish_via_get_changes_nothing(self):
        self.client.login(username='tester', password='geheim123')
        self.client.get(f'/post/{self.draft.pk}/publish/')
        self.draft.refresh_from_db()
        self.assertIsNone(self.draft.published_date)

    def test_publish_via_post_works(self):
        self.client.login(username='tester', password='geheim123')
        self.client.post(f'/post/{self.draft.pk}/publish/')
        self.draft.refresh_from_db()
        self.assertIsNotNone(self.draft.published_date)
