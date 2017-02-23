from django.db import models
# Create your models here.


class CustomPermission(models.Model):  # Abstract model to add custom permissions
    class Meta:
        permissions = (
            ("custom_permission_1", "Custom permission_1"),
            ("custom_permission_2", "Custom permission_2"),
            ("custom_permission_3", "Custom permission_3"),
        )