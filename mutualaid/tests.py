from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from mutualaid.models import *


class CommunityResourceApiTests(APITestCase):
    def test_get_by_location(self):
        data = {
            'resource_type': 'FOOD_PANTRY',
            'address': 'Some Address',
            'location': Point(-118.24268, 34.05369) # Los Angeles City Hall
        }
        CommunityResource.objects.create(**data)
        self.assertEqual(1, CommunityResource.objects.count())

        # 34.05626, -118.23652, Los Angeles Union Station, 0.4mi/0.64km away.
        # With radius 1 from Union Station, we expect to see the City Hall based on lat/lon.
        # With radius 0.1, we expect it would be filtered out.
        query_params = {
            'latitude': '34.05626',
            'longitude': '-118.23652',
            'radius': '1',
        }
        response = self.client.get('/api/community-resources/', query_params)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['count'])
        self.assertEqual(1, len(response.data['results']))

        query_params = {
            'latitude': '34.05626',
            'longitude': '-118.23652',
            'radius': '0.1',
        }
        response = self.client.get('/api/community-resources/', query_params)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.data['count'])
        self.assertEqual(0, len(response.data['results']))



