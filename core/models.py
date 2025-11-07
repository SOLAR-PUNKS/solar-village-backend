from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models


# Subclass the default User early as changing it later can be hard. Version 5.1 and onward of the django docs stopped
# saying it was highly recommended. TODO: Read up on that.
# PR which changed it: https://github.com/django/django/pull/18566
# discussion: https://forum.djangoproject.com/t/what-does-the-community-think-to-carltons-take-on-auth-user/34672/5
# post which seems to have spawned the change: https://buttondown.com/carlton/archive/evolving-djangos-authuser/
class User(AbstractUser):
    pass


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
        User,
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
