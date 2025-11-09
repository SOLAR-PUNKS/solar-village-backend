from django.contrib.auth import get_user_model
from django.contrib.gis.db import models


# Create your models here.
class MutualAidPost(models.Model):
    POST_TYPE_CHOICES = [
        ('OFFER', 'Offer'),
        ('REQUEST', 'Request'),
    ]

    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('CLOTHING', 'Clothing'),
        ('SHELTER', 'Shelter'),
        ('TRANSPORTATION', 'Transportation'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('FULFILLED', 'Fulfilled'),
        ('EXPIRED', 'Expired'),
    ]

    type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    location = models.PointField(geography=True)
    address = models.CharField(max_length=500, blank=True)
    contact_info = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='mutual_aid_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['type', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"


class CommunityResource(models.Model):
    """
    Generic model for community resources (food pantries, shelters, etc.).
    Managed by backend data ingestion service, not via UI.
    """
    RESOURCE_TYPE_CHOICES = [
        ('FOOD_PANTRY', 'Food Pantry'),
        # Future resource types can be added here:
        # ('SHELTER', 'Shelter'),
        # ('CLINIC', 'Health Clinic'),
        # ('LIBRARY', 'Library'),
        # etc.
    ]

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        help_text="Type of community resource"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.PointField(geography=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    hours = models.JSONField(
        blank=True,
        null=True,
        help_text="Structured operating hours. Format: {'monday': {'open': '09:00', 'close': '17:00'}, ...}",
        default=dict
    )
    eligibility_requirements = models.TextField(blank=True, help_text="Eligibility requirements for this resource")
    services = models.TextField(blank=True, help_text="Additional services offered")
    is_active = models.BooleanField(default=True, help_text="Whether this resource is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Community Resources'
        indexes = [
            models.Index(fields=['resource_type', 'is_active']),
            models.Index(fields=['is_active']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.get_resource_type_display()}: {self.name}"

    def get_hours_display(self):
        """
        Convert structured hours JSON to human-readable format.
        Returns a formatted string of operating hours.
        """
        if not self.hours:
            return "Hours not specified"

        def format_time_slot(slot):
            """Format a single time slot dict to string."""
            if isinstance(slot, dict):
                if 'open' in slot and 'close' in slot:
                    return f"{slot['open']} - {slot['close']}"
                elif slot.get('open_24h'):
                    return "24 Hours"
            return None

        formatted_hours = []
        for day_key, day_data in self.hours.items():
            if day_data is None:
                continue

            day_name = day_key.capitalize()  # Convert 'monday' -> 'Monday'

            if day_data == 'closed':
                formatted_hours.append(f"{day_name}: Closed")
            elif isinstance(day_data, dict):
                slot_str = format_time_slot(day_data)
                if slot_str:
                    formatted_hours.append(f"{day_name}: {slot_str}")
            elif isinstance(day_data, list):
                # Handle multiple time slots per day
                slots = [format_time_slot(slot) for slot in day_data if format_time_slot(slot)]
                if slots:
                    formatted_hours.append(f"{day_name}: {', '.join(slots)}")

        return '\n'.join(formatted_hours) if formatted_hours else "Hours not specified"
