from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_main and Organization.objects.exclude(pk=self.pk).filter(is_main=True).exists():
            raise ValidationError("There can only be one main organization")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Role(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('EDITOR', 'Editor'),
        ('VIEWER', 'Viewer'),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        related_name='users'
    )
    
    def is_organization_admin(self):
        return self.role and self.role.name == 'ADMIN'

    def is_main_org_admin(self):
        return (self.organization is not None and 
                self.organization.is_main and 
                self.is_organization_admin())

    def is_editor(self):
        return self.role and self.role.name == 'EDITOR'

    def is_viewer(self):
        return self.role and self.role.name == 'VIEWER'