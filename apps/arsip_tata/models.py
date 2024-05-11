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
    # box_number = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1)]
    # )
    box_number = models.CharField(max_length=10)
    yeardate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2023), MaxValueValidator(2050)]
    )

    year = models.ForeignKey(
        Year,
        db_column='year_id',
        on_delete=models.CASCADE, 
        default=None
    )        
    class Meta:
        unique_together = ('box_number', 'yeardate')    
    
    
    def __str__(self) -> str:
        return f"{self.box_number}/{self.year.yeardate}"

class Bundlecode(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Bundle(models.Model):
    id = models.AutoField(primary_key=True)
    bundle_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    code = models.CharField(max_length=10)
    creator = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    year_bundle = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900),MaxValueValidator(2050)]
    )
    yeardate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2023), MaxValueValidator(2050)]
    )
   
    box = models.ForeignKey(
        Box,
        db_column='box_id',
        on_delete=models.CASCADE, 
        default=None
    )        
   
    # bundlecode = models.ForeignKey(
    #     Bundlecode,
    #     db_column='bundlecode_id',
    #     on_delete=models.CASCADE, 
    #     default=None
    # )        
    
    class Meta:
        unique_together = ('bundle_number', 'yeardate')    


    def __str__(self) -> str:
        return f"{self.bundle_number}_{self.box.box_number}_{self.id}"

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
        validators=[MinValueValidator(0)], default=0
    )
    original = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    total = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    accesstype = models.CharField(max_length=2, choices=ACCESS_CHOICES, default='T')
    yeardate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2023), MaxValueValidator(2050)]
    )
    codegen = models.CharField(max_length=20, blank=True, null=True, unique=True)
    bundle = models.ForeignKey(
        Bundle,
        db_column='bundle_id',
        on_delete=models.CASCADE, 
        default=None
    )        
    class Meta:
        unique_together = ('item_number', 'yeardate')    

    def __str__(self) -> str:
        return f"{self.item_number}_{self.bundle.bundle_number}_{self.id}"


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='images', null=True, blank=True)
    idcard = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Trans(models.Model):
    id = models.AutoField(primary_key=True)
    codetrans = models.CharField(max_length=8, unique=True, null=True)
    date_trans = models.DateField()
    customer = models.ForeignKey(
        Customer,
        db_column='customer_id',
        on_delete=models.CASCADE, 
        default=None
    )        


    def __str__(self) -> str:
        return f"{self.customer.name}_{self.date_trans}"


class TransDetail(models.Model):
    id = models.AutoField(primary_key=True)
    date_return = models.DateField(null=True, blank=True)
    
    item = models.ForeignKey(
        Item,
        db_column='item_id',
        on_delete=models.CASCADE, 
        default=None
    )
    
    trans = models.ForeignKey(
        Trans,
        db_column='trans_id',
        on_delete=models.CASCADE, 
        default=None
    )        

    def __str__(self) -> str:
        return f"{self.item.title}_{self.date_return}"
