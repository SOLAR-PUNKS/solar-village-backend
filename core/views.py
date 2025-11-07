from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import MutualAidPost
from .serializers import MutualAidPostSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit/delete their posts."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.created_by == request.user


class MutualAidPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing MutualAidPost instances.
    """
    queryset = MutualAidPost.objects.all()
    serializer_class = MutualAidPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = MutualAidPost.objects.all()

        # Filter by status (default to ACTIVE if not specified)
        status = self.request.query_params.get('status', 'ACTIVE')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by type
        post_type = self.request.query_params.get('type', None)
        if post_type:
            queryset = queryset.filter(type=post_type)

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filter by location (distance-based)
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        radius = self.request.query_params.get('radius', None)

        if latitude and longitude and radius:
            try:
                lat = float(latitude)
                lng = float(longitude)
                radius_km = float(radius)

                # Validate coordinates
                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    return queryset.none()

                # Create point from coordinates
                user_location = Point(lng, lat, srid=4326)

                # Filter by distance using PostGIS
                queryset = queryset.annotate(
                    distance=Distance('location', user_location)
                ).filter(
                    location__distance_lte=(user_location, D(km=radius_km))
                ).order_by('distance')
            except (ValueError, TypeError):
                # Invalid parameters, return empty queryset
                return queryset.none()

        return queryset

    def perform_create(self, serializer):
        """Set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)
