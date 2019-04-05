import os
import markdown as md

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='blog',
        default=os.path.join('blog', 'default_category.jpg')
    )

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="70" />')
    image_tag.short_description = "Image"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    on_publish = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(
        upload_to='blog',
        default=os.path.join('blog', 'default_post.jpg')
    )
    n_views = models.IntegerField(default=0)
    tags = models.CharField(max_length=100, default='')

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="70px" />')
    image_tag.short_description = "Image"

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    description = models.TextField(null=True)
    image = models.ImageField(
        upload_to='blog',
        default=os.path.join('blog', 'default_profile.jpg')
    )

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="70px" />')
    image_tag.short_description = "Image"

    def __str__(self):
        return str(self.user)


class Subscriber(models.Model):
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Subscriber)
def save_subscriber(sender, instance, **kwargs):
    send_mail(
        "New post",
        f"Hi {instance}, You subscribe complete. We send new post evry day",
        "Yeudev.com",
        [str(instance)],
    )
    instance.save()

