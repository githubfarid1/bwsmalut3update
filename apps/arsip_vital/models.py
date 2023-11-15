from django.db import models
import uuid
# Create your models here.
class Variety(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    folder = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Doc(models.Model):
    id = models.AutoField(primary_key=True)
    doc_number = models.SmallIntegerField(null=True)
    name = models.TextField(null=True, blank=True)
    work_unit = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=4, null=True, blank=True)
    media = models.CharField(max_length=50, null=True, blank=True)
    countstr = models.CharField(max_length=100, null=True, blank=True)
    save_life = models.CharField(max_length=100, null=True, blank=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    save_location = models.TextField(null=True, blank=True)
    protect_method = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    filesize = models.IntegerField(null=True)
    page_count = models.SmallIntegerField(null=True)

    variety = models.ForeignKey(
        Variety,
        db_column='variety_id',
        on_delete=models.CASCADE,
        related_name="varieties"
    )        
    def __str__(self) -> str:
        return f'{self.variety.name}_{self.name}'
