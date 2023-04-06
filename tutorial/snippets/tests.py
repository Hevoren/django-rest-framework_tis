from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet


class SnippetModelTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.snippet_data = {
            'title': 'Test Snippet',
            'code': 'print("Hello, World!")',
            'linenos': True,
            'language': 'python',
            'style': 'friendly'
        }
        self.snippet = Snippet.objects.create(owner=self.user, **self.snippet_data)

    def test_create_snippet(self):
        url = reverse('snippet-list')
        response = self.client.post(url, self.snippet_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 2)
        self.assertEqual(Snippet.objects.get(id=response.data['id']).title, 'Test Snippet')

    def test_delete_snippet(self):
        url = reverse('snippet-detail', args=[self.snippet.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

    def test_update_snippet(self):
        url = reverse('snippet-detail', args=[self.snippet.id])
        updated_data = {
            'title': 'Updated Snippet',
            'code': 'print("Updated Hello, World!")',
            'linenos': False,
            'language': 'python',
            'style': 'friendly'
        }
        response = self.client.put(url, updated_data, format='json')