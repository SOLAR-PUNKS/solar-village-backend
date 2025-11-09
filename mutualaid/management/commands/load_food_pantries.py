"""
Management command to load sample food pantry data into the database.
This command is used for seeding the database with test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from mutualaid.models import CommunityResource


class Command(BaseCommand):
    help = 'Load sample food pantry data into the database'

    def handle(self, *args, **options):
        """Create sample food pantry records."""
        pantries_data = [
            {
                'resource_type': 'FOOD_PANTRY',
                'name': 'Community Food Bank',
                'description': 'A community-run food bank serving local residents in need.',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'address': '123 Main Street',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'phone': '(212) 555-0100',
                'email': 'info@communityfoodbank.org',
                'website': 'https://www.communityfoodbank.org',
                'hours': {
                    'monday': {'open': '09:00', 'close': '17:00'},
                    'tuesday': {'open': '09:00', 'close': '17:00'},
                    'wednesday': {'open': '09:00', 'close': '17:00'},
                    'thursday': {'open': '09:00', 'close': '17:00'},
                    'friday': {'open': '09:00', 'close': '17:00'},
                    'saturday': {'open': '10:00', 'close': '14:00'},
                    'sunday': 'closed',
                },
                'eligibility_requirements': 'Open to all community members in need. No ID required.',
                'services': 'Food distribution, emergency food assistance, nutrition education',
                'is_active': True,
            },
            {
                'resource_type': 'FOOD_PANTRY',
                'name': 'Hope Pantry',
                'description': 'Providing food assistance and support to families in the area.',
                'latitude': 40.7589,
                'longitude': -73.9851,
                'address': '456 Broadway',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10013',
                'phone': '(212) 555-0200',
                'email': 'contact@hopepantry.org',
                'website': 'https://www.hopepantry.org',
                'hours': {
                    'monday': 'closed',
                    'tuesday': {'open': '10:00', 'close': '16:00'},
                    'wednesday': {'open': '10:00', 'close': '16:00'},
                    'thursday': {'open': '10:00', 'close': '16:00'},
                    'friday': 'closed',
                    'saturday': {'open': '09:00', 'close': '13:00'},
                    'sunday': 'closed',
                },
                'eligibility_requirements': 'Must provide proof of address. Income-based eligibility.',
                'services': 'Food distribution, fresh produce, canned goods, baby formula',
                'is_active': True,
            },
            {
                'resource_type': 'FOOD_PANTRY',
                'name': 'Neighborhood Food Share',
                'description': 'A neighborhood-based food sharing program.',
                'latitude': 40.7282,
                'longitude': -73.9942,
                'address': '789 Park Avenue',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10021',
                'phone': '(212) 555-0300',
                'email': 'info@neighborhoodfoodshare.org',
                'website': '',
                'hours': {
                    'monday': {'open': '11:00', 'close': '15:00'},
                    'tuesday': 'closed',
                    'wednesday': {'open': '11:00', 'close': '15:00'},
                    'thursday': 'closed',
                    'friday': {'open': '11:00', 'close': '15:00'},
                    'saturday': 'closed',
                    'sunday': 'closed',
                },
                'eligibility_requirements': 'Open to all. No requirements.',
                'services': 'Food distribution, community meals',
                'is_active': True,
            },
            {
                'resource_type': 'FOOD_PANTRY',
                'name': 'Sunshine Food Pantry',
                'description': 'Serving the community with dignity and respect.',
                'latitude': 40.7505,
                'longitude': -73.9934,
                'address': '321 5th Avenue',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10016',
                'phone': '(212) 555-0400',
                'email': 'sunshine@foodpantry.org',
                'website': 'https://www.sunshinefoodpantry.org',
                'hours': {
                    'monday': {'open': '08:00', 'close': '18:00'},
                    'tuesday': {'open': '08:00', 'close': '18:00'},
                    'wednesday': {'open': '08:00', 'close': '18:00'},
                    'thursday': {'open': '08:00', 'close': '18:00'},
                    'friday': {'open': '08:00', 'close': '18:00'},
                    'saturday': 'closed',
                    'sunday': 'closed',
                },
                'eligibility_requirements': 'Must be a resident of the area. Proof of residency required.',
                'services': 'Food distribution, holiday meal assistance, senior food program',
                'is_active': True,
            },
            {
                'resource_type': 'FOOD_PANTRY',
                'name': 'Unity Community Kitchen',
                'description': 'Providing meals and food assistance to those in need.',
                'latitude': 40.7614,
                'longitude': -73.9776,
                'address': '654 Lexington Avenue',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10022',
                'phone': '(212) 555-0500',
                'email': 'unity@communitykitchen.org',
                'website': '',
                'hours': {
                    'monday': {'open': '12:00', 'close': '18:00'},
                    'tuesday': {'open': '12:00', 'close': '18:00'},
                    'wednesday': {'open': '12:00', 'close': '18:00'},
                    'thursday': {'open': '12:00', 'close': '18:00'},
                    'friday': {'open': '12:00', 'close': '18:00'},
                    'saturday': {'open': '12:00', 'close': '18:00'},
                    'sunday': {'open': '12:00', 'close': '18:00'},
                },
                'eligibility_requirements': 'Open to all. No requirements.',
                'services': 'Hot meals, food pantry, community kitchen',
                'is_active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for pantry_data in pantries_data:
            latitude = pantry_data.pop('latitude')
            longitude = pantry_data.pop('longitude')
            location = Point(longitude, latitude, srid=4326)

            resource, created = CommunityResource.objects.update_or_create(
                name=pantry_data['name'],
                resource_type=pantry_data['resource_type'],
                defaults={
                    **pantry_data,
                    'location': location,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created community resource: {resource.name} ({resource.get_resource_type_display()})'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Updated community resource: {resource.name} ({resource.get_resource_type_display()})'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully loaded community resources. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )

