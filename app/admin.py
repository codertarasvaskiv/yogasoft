from django.contrib import admin
from . import models


class ProjectsView(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', ]


class BlogsView(admin.ModelAdmin):
    list_display = ['author', 'name']


class TagView(admin.ModelAdmin):
    list_display = ['name']


class CommentView(admin.ModelAdmin):
    list_display = ['author_name', 'blog', 'time']



admin.site.register(models.Comment, CommentView)
#admin.site.register(models.CommentSecondLevel, CommentView)
admin.site.register(models.BlogPostImage)
admin.site.register(models.Tag, TagView)
admin.site.register(models.BlogPost, BlogsView)
admin.site.register(models.Project, ProjectsView)

# Register your models here.
