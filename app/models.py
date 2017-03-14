from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class CustomPermission(models.Model):  # Abstract model to add custom permissions
    class Meta:
        permissions = (
            ("blog_admin", "Blog administration"),
            ("portfolio_admin", "Portfolio administration"),
            ("testimonials_admin", "Testimonials administration"),
            ("projects_admin", "Projects administration"),
            ("user_messages", "Permission to see customer messages"),
            ("admin_users", "Admin users administration"),
            ("general_users", "General users administration"),
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


class UserYoga(models.Model):  # Extends base user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # Is site administrator
    auth_by_sn = models.BooleanField(default=True)  # Authenticated by social network
    extra_data = models.CharField(max_length=200, blank=True)


def create_profile(sender, **kwargs):  # Function that synchronizes extended user model creation with base model
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserYoga(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)


class PortfolioContent(models.Model):
    name = models.CharField(unique=True, max_length=250)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    technologies = models.CharField(max_length=250)
    link = models.CharField(max_length=250, blank=True)
    client = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return str(self.name)


class ImageContentClass(models.Model):
    image = models.ImageField(upload_to='content_images')
    content = models.ForeignKey(PortfolioContent, on_delete=models.CASCADE)


class BlogPost(models.Model):
    author = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.author) + '/' + self.name


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
    date = models.DateTimeField(auto_now_add=True)


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


class ContactUsModel(models.Model):
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
