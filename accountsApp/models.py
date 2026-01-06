from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    # Override to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='accountsApp_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accountsApp_user_set',
        related_query_name='user',
    )
