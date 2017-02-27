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

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='tech_images')


class UserYoga(models.Model):
    user = models.OneToOneField(User)
    extra_data = models.CharField(max_length=200)


class PortfolioContent(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    technologies = models.CharField(max_length=250)
    link = models.CharField(max_length=250, blank=True)
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

    def __str__(self):
        return str(self.content.name)


class Testimonial(models.Model):
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

    def __str__(self):  # just for debug, remove later
        return self.message


class CommentSecondLevel(models.Model):
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)
    father_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):  # just for debug, remove later
        return self.message
