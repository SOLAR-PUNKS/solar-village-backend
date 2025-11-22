from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import MutualAidPost, CommunityResource


class MutualAidPostSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    location = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MutualAidPost
        fields = [
            'id',
            'type',
            'title',
            'description',
            'category',
            'status',
            'location',
            'latitude',
            'longitude',
            'address',
            'contact_info',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_location(self, obj):
        """Convert PointField to lat/lng dict for API output."""
        if obj.location:
            return {
                'latitude': obj.location.y,
                'longitude': obj.location.x,
            }
        return None

    def validate_latitude(self, value):
        """Validate latitude is in valid range."""
        if not -90 <= value <= 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )
        return value

    def validate_longitude(self, value):
        """Validate longitude is in valid range."""
        if not -180 <= value <= 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )
        return value

    def create(self, validated_data):
        """Create post with location from lat/lng."""
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        validated_data['location'] = Point(longitude, latitude, srid=4326) # degrees
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update post with location from lat/lng if provided."""
        if 'latitude' in validated_data and 'longitude' in validated_data:
            latitude = validated_data.pop('latitude')
            longitude = validated_data.pop('longitude')
            validated_data['location'] = Point(longitude, latitude, srid=4326) # degrees
        return super().update(instance, validated_data)


class CommunityResourceSerializer(serializers.ModelSerializer):
    """Serializer for CommunityResource model - read-only for API consumers."""
    location = serializers.SerializerMethodField()
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)
    hours_display = serializers.SerializerMethodField()

    class Meta:
        model = CommunityResource
        fields = [
            'id',
            'resource_type',
            'resource_type_display',
            'name',
            'description',
            'location',
            'address',
            'city',
            'state',
            'zip_code',
            'phone',
            'email',
            'website',
            'hours',
            'hours_display',
            'special_hours',
            'eligibility_requirements',
            'services',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_location(self, obj):
        """Convert PointField to lat/lng dict for API output."""
        if obj.location:
            return {
                'latitude': obj.location.y,
                'longitude': obj.location.x,
            }
        return None

    def get_hours_display(self, obj):
        """Return human-readable formatted hours."""
        return obj.get_hours_display()
