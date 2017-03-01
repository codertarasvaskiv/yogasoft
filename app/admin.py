from django.contrib import admin
from . import models


class ProjectsView(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name',]


admin.site.register(models.Project, ProjectsView)

# Register your models here.
admin.site.register(models.Testimonial)
admin.site.register(models.UserYoga)
