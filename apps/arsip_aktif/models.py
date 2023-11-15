from django.db import models
import uuid
   

class Variety(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    folder = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Bundle(models.Model):
    id = models.AutoField(primary_key=True)
    bundle_number = models.SmallIntegerField()
    code = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.box_number}_{self.bundle_number}_{self.code}'
    variety = models.ForeignKey(
        Variety,
        db_column='variety_id',
        on_delete=models.CASCADE,
        related_name="varieties"
    )        

class Doc(models.Model):
    id = models.AutoField(primary_key=True)
    doc_number = models.SmallIntegerField(null=True)
    name = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    count = models.IntegerField(null=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    orinot = models.CharField(max_length=4, null=True, blank=True)
    access = models.CharField(max_length=50, null=True, blank=True)

    bundle = models.ForeignKey(
        Bundle,
        db_column='bundle_id',
        on_delete=models.CASCADE, 
        related_name='docs'
    )
    def __str__(self) -> str:
        return f'{self.name}'
