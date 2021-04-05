from django.test import TestCase
from django.urls import reverse

from explorer.models import Collections


class IndexViewTestCase(TestCase):

    def test_index(self):
        Collections.objects.create(filename='test.csv')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Collection Listing")

