from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Dream

User = get_user_model()
PASSWORD = 'pass12345-test'


class DreamTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', password=PASSWORD)
        self.bob = User.objects.create_user('bob', password=PASSWORD)
        self.public = Dream.objects.create(user=self.alice, text='ommaviy-orzu-abc')
        self.private = Dream.objects.create(
            user=self.alice, text='gizli-orzu-xyz', visibility=Dream.Visibility.PRIVATE
        )

    def test_feed_hides_private(self):
        response = self.client.get(reverse('feed'))
        self.assertContains(response, 'ommaviy-orzu-abc')
        self.assertNotContains(response, 'gizli-orzu-xyz')

    def test_private_detail_is_404_for_others(self):
        self.client.login(username='bob', password=PASSWORD)
        response = self.client.get(reverse('dream_detail', args=[self.private.pk]))
        self.assertEqual(response.status_code, 404)

    def test_owner_sees_private(self):
        self.client.login(username='alice', password=PASSWORD)
        response = self.client.get(reverse('dream_detail', args=[self.private.pk]))
        self.assertEqual(response.status_code, 200)

    def test_only_owner_can_edit(self):
        self.client.login(username='bob', password=PASSWORD)
        response = self.client.get(reverse('dream_update', args=[self.public.pk]))
        self.assertEqual(response.status_code, 403)

    def test_empty_dream_is_rejected(self):
        self.client.login(username='alice', password=PASSWORD)
        before = Dream.objects.count()
        response = self.client.post(reverse('dream_create'), {
            'text': '   ', 'stage': 'idea', 'visibility': 'public',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Dream.objects.count(), before)

    def test_text_only_dream_is_created(self):
        self.client.login(username='alice', password=PASSWORD)
        response = self.client.post(reverse('dream_create'), {
            'text': 'yangi orzu', 'stage': 'idea', 'visibility': 'public',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dream.objects.filter(text='yangi orzu', user=self.alice).exists())

    def test_achieved_sets_date(self):
        dream = Dream.objects.create(user=self.alice, text='x', stage=Dream.Stage.ACHIEVED)
        self.assertIsNotNone(dream.achieved_at)
        dream.stage = Dream.Stage.IDEA
        dream.save()
        self.assertIsNone(dream.achieved_at)
