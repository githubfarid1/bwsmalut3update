from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Year(models.Model):
    id = models.AutoField(primary_key=True)
    yeardate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2023), MaxValueValidator(2050)], unique=True
    )

    def __str__(self) -> str:
        return self.yeardate

class Box(models.Model):
    id = models.AutoField(primary_key=True)
    box_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    year = models.ForeignKey(
        Year,
        db_column='year_id',
        on_delete=models.CASCADE, 
        default=None
    )        
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['box_number', 'year_id'], name="unique_box_number_year"
            )
        ]
    def __str__(self) -> str:
        return f"{self.box_number}_{self.year.yeardate}"


class Bundle(models.Model):
    id = models.AutoField(primary_key=True)
    bundle_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    code = models.CharField(max_length=10)
    creator = models.CharField(max_length=255)
    decription = models.TextField(null=True, blank=True)
    year_bundle = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900),MaxValueValidator(2050)]
    )
   
    box = models.ForeignKey(
        Box,
        db_column='box_id',
        on_delete=models.CASCADE, 
        default=None
    )        

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bundle_number', 'box_id'], name="unique_bundle_number_box"
            )
        ]

    def __str__(self) -> str:
        return f"{self.bundle_number}_{self.box.box_number}"


class Item(models.Model):
    ACCESS_CHOICES = (
        ('B', 'Biasa'),
        ('T', 'Terbatas'),
        ('R', 'Rahasia'),

    )
    id = models.AutoField(primary_key=True)
    item_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    title = models.CharField(max_length=255)
    copy = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    original = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    total = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    accesstype = models.CharField(max_length=2, choices=ACCESS_CHOICES, default='T')
    
    bundle = models.ForeignKey(
        Bundle,
        db_column='bundle_id',
        on_delete=models.CASCADE, 
        default=None
    )        
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['item_number', 'bundle_id'], name="unique_item_number_bundle"
            )
        ]

    def __str__(self) -> str:
        return f"{self.item_number}_{self.bundle.bundle_number}"
