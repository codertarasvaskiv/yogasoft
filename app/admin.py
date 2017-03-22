from django.contrib import admin
from . import models


class ProjectsView(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', ]


class BlogsView(admin.ModelAdmin):
    list_display = ['author', 'name', 'text', 'nameUA', 'textUA']


class TagView(admin.ModelAdmin):
    list_display = ['name']


class CommentView(admin.ModelAdmin):
    list_display = ['author_name', 'time']


class PortfolioContentView(admin.ModelAdmin):
    list_display = ['name', 'description', 'link', 'client']


class ImageContentView(admin.ModelAdmin):
    list_display = ['content', 'image']


class UserYogaView(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']


class TechnologyView(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']


# Register your models here.
admin.site.register(models.PortfolioContent, PortfolioContentView)
admin.site.register(models.ImageContentClass, ImageContentView)
admin.site.register(models.Comment, CommentView)
admin.site.register(models.CommentSecondLevel, CommentView)
admin.site.register(models.BlogPostImage)
admin.site.register(models.Tag, TagView)
admin.site.register(models.BlogPost, BlogsView)
admin.site.register(models.Project, ProjectsView)
admin.site.register(models.ContactUsModel)
admin.site.register(models.Testimonial)
admin.site.register(models.Technology, TechnologyView)
admin.site.register(models.UserYoga)
