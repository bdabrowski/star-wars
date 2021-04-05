import os

from django.test import TestCase
from django.urls import reverse

from explorer.models import Collections


test_csv = """\
name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld,date
Luke Skywalker,172,77,blond,fair,blue,19BBY,male,Tatooine,2014-12-20
C-3PO,167,75,n/a,gold,yellow,112BBY,n/a,Tatooine,2014-12-20
R2-D2,96,32,n/a,"white, blue",red,33BBY,n/a,Naboo,2014-12-20
Darth Vader,202,136,none,white,yellow,41.9BBY,male,Tatooine,2014-12-20
"""


class CountingViewTestCase(TestCase):
    def setUp(self):
        with open('explorer/data/example.csv', 'w') as f:
            f.write(test_csv)

    def tearDown(self):
        os.remove('explorer/data/example.csv')

    def test_index(self):
        col = Collections.objects.create(filename='example.csv')
        response = self.client.get(reverse('counting', kwargs={'collection_id': col.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Luke Skywalke")
        self.assertContains(response, "C-3PO")
        self.assertContains(response, "R2-D2")
        self.assertContains(response, "Darth Vader")