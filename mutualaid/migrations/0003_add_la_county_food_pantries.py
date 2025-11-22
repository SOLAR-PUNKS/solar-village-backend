from django.core.management import call_command
from django.db import migrations


def add_la_county_food_pantries(apps, schema_editor):
    call_command("load_la_food_pantries")


class Migration(migrations.Migration):
    dependencies = [
        ("mutualaid", "0002_communityresource_special_hours"),
    ]

    operations = [
        migrations.RunPython(add_la_county_food_pantries),
    ]