from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CustomPermission(models.Model):  # Abstract model to add custom permissions
    class Meta:
        permissions = (
            ("custom_permission_1", "Custom permission_1"),
            ("custom_permission_2", "Custom permission_2"),
            ("custom_permission_3", "Custom permission_3"),
        )


class Project(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    query = models.TextField()
    file = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=50)


# this is like python, php, wordpres, drupal
class Technology(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='tech_images')


class UserYoga(models.Model):
    user = models.OneToOneField(User)
    extra_data = models.CharField(max_length=200)


class PortfolioContent(models.Model):
    """ this class represents examples of sites our company has done"""
    name = models.CharField(max_length=40, unique=True)

    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    technologies = models.CharField(max_length=250)  # why not many to many with Technology ?
    link = models.CharField(max_length=250, blank=True)  # why do we need this ?
    client = models.CharField(max_length=250, blank=True)


class ImageContentClass(models.Model):
    image = models.ImageField(upload_to='content_images')
    content = models.ForeignKey(PortfolioContent, on_delete=models.CASCADE)


class BlogPost(models.Model):
    author = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)


class BlogPostImage(models.Model):
    image = models.ImageField(upload_to='content_images')
    content = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class Testimonial(models.Model):
    """ it is like award, proof  відгук"""
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    is_moderated = models.BooleanField(default=False)


class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class CommentSecondLevel(models.Model):
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)
    father_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)



