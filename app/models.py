from django.db import models

# Create your models here.


class CustomPermission(models.Model):  # Abstract model to add custom permissions
    class Meta:
        permissions = (
            ("custom_permission_1", "Custom permission_1"),
            ("custom_permission_2", "Custom permission_2"),
            ("custom_permission_3", "Custom permission_3"),
        )


class StartProject(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    query = models.TextField()
    file = models.CharField(max_length=255)

