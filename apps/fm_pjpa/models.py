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


class Subfolder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # link = models.CharField(max_length=50, unique=True)
    year = models.CharField(max_length=4, validators=[MinLengthValidator(4)], default='2023')
    folder = models.CharField(max_length=50)
    create_date = models.DateTimeField(null=True, blank=True)
    
    department = models.ForeignKey(
        Department,
        db_column='department_id',
        on_delete=models.CASCADE, 
        # related_name='pjpa_departments',
        default=None
    )        

    def __str__(self) -> str:
        return self.name

