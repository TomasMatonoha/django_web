from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Location name",
                            help_text="Enter a location name",
                            error_messages={'blank': "Enter a location",
                                            'unique': "Enter a unique location"})
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                 error_messages={'blank': "Enter a latitude"})
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                  error_messages={'blank': "Enter a longitude"})
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', 'latitude', 'longitude']
        verbose_name = 'Location'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name="Post title",
                             help_text="Enter a title",
                             error_messages={"blank": "Enter a title"})
    content = models.TextField(verbose_name="Post text",
                               help_text="Enter post text",
                               error_messages={"blank": "Enter post text"})
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Post author")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Post created at")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Post updated at")
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE,
                                 verbose_name="Post location",
                                 error_messages={"blank": "Enter post location"})
    image = models.ImageField(upload_to='post_media',
                              verbose_name='Post image',
                              blank=True,
                              null=True)

    class Meta:
        ordering = ['-created_at', '-updated_at', 'title', 'location', 'author']
        verbose_name = 'Post'

    def __str__(self):
        return self.title
