from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(null=True, max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Specify related_name for user_permissions and groups
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users_permissions')
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users_groups')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'dob']

    def __str__(self):
        return self.email


