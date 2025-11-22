from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from mutualaid.models import *


class CommunityResourceApiTests(APITestCase):
    def test_get_by_location(self):
        # Make some entry for middle of pacific and test location there.
        # Added a data migration for LA food pantries so test database will have those entries for now.
        data = {
            'resource_type': 'FOOD_PANTRY',
            'address': 'The Pacific',
            'location': Point(-155.42032, 48.25744)  # Pacific ocean
        }

        CommunityResource.objects.create(**data)

        # 48.26144, -155.42432 is 0.3mi/0.53km away.
        # With radius 1 from the first point, we expect to see this based on lat/lon.
        # With radius 0.1, we expect it would be filtered out.
        query_params = {
            'latitude': '48.26144',
            'longitude': '-155.42432',
            'radius': '1.0',
        }
        response = self.client.get('/api/community-resources/', query_params)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['count'])
        self.assertEqual(1, len(response.data['results']))

        query_params = {
            'latitude': '48.26144',
            'longitude': '-155.42432',
            'radius': '0.1',
        }
        response = self.client.get('/api/community-resources/', query_params)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.data['count'])
        self.assertEqual(0, len(response.data['results']))
