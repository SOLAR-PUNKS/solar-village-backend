from django.contrib.auth.models import AbstractUser


# Subclass the default User early as changing it later can be hard. Version 5.1 and onward of the django docs stopped
# saying it was highly recommended. TODO: Read up on that.
# PR which changed it: https://github.com/django/django/pull/18566
# discussion: https://forum.djangoproject.com/t/what-does-the-community-think-to-carltons-take-on-auth-user/34672/5
# post which seems to have spawned the change: https://buttondown.com/carlton/archive/evolving-djangos-authuser/
class User(AbstractUser):
    pass
