from django.db import models
import uuid
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    shortname = models.CharField(max_length=30, unique=True, default=None)
    # link = models.CharField(max_length=40, unique=True)
    folder = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, max_length=40, default=None)
    create_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


