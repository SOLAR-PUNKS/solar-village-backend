from collections import namedtuple
import csv
import os
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from mutualaid.models import CommunityResource


LAFoodPantry = namedtuple(
    "LAFoodPantry",
    ["name", "notes", "address_short", "city_state_zip", "address_consolidated", "latitude", "longitude"]
)


class Command(BaseCommand):

    help = "Load the Food Pantries in Los Angeles County"

    def handle(self, *args, **kwargs):
        csv_location = os.path.join(settings.BASE_DIR, "data", "Los_Angeles_County_Foodbanks_with_coords.csv")
        la_food_pantries = []
        with open(csv_location, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader)  # Skip the header row
            for row in reader:
                record = LAFoodPantry(*row)
                # Column formatted as "city, state zip, United States", e.g. 'Compton, CA 90222, United States'
                # Sometimes extra stuff is at the beginning, so grab from the end with [-1] etc.
                address_portions = record.city_state_zip.split(',')
                city = address_portions[-3].strip()
                state, zipcode = address_portions[-2].strip().split(' ')
                la_food_pantries.append({
                    'name': record.name,
                    'resource_type': 'FOOD_PANTRY',
                    'special_hours': record.notes,
                    'address': record.address_short,
                    'city': city,
                    'state': state,
                    'zip_code': zipcode,
                    'latitude': record.latitude,
                    'longitude': record.longitude
                })
        self.stdout.write(
            self.style.SUCCESS(f"Read {len(la_food_pantries)} Food Pantry records from CSV")
        )

        created_count = 0
        updated_count = 0

        for food_pantry in la_food_pantries:
            latitude = float(food_pantry.pop('latitude'))
            longitude = float(food_pantry.pop('longitude'))
            location = Point(longitude, latitude, srid=4326)
            resource, created = CommunityResource.objects.update_or_create(
                name=food_pantry['name'],
                resource_type=food_pantry['resource_type'],
                address=food_pantry['address'],
                defaults={
                    **food_pantry,
                    'location': location,
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded LA Food Pantries.\n'
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )
