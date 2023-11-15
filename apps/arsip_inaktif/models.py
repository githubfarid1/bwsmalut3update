from django.db import models
import uuid
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    defcode = models.CharField(max_length=20, unique=True)
    link = models.CharField(max_length=50, unique=True)
    folder = models.CharField(max_length=50, unique=True)


    def __str__(self) -> str:
        return self.name

class Bundle(models.Model):
    id = models.AutoField(primary_key=True)
    box_number = models.SmallIntegerField()
    bundle_number = models.SmallIntegerField()
    code = models.CharField(max_length=20, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    orinot = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    department = models.ForeignKey(
        Department,
        db_column='department_id',
        on_delete=models.CASCADE,
        related_name="bundles"
    )        
    def __str__(self) -> str:
        return f'{self.box_number}_{self.bundle_number}_{self.title}'


class Doc(models.Model):
    id = models.AutoField(primary_key=True)
    doc_number = models.SmallIntegerField()
    doc_count = models.SmallIntegerField(null=True)
    orinot = models.CharField(max_length=10, null=True, blank=True)
    doc_type = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    filesize = models.IntegerField(null=True)
    page_count = models.SmallIntegerField(null=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    access = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.doc_number}_{self.description}'

    bundle = models.ForeignKey(
        Bundle,
        db_column='bundle_id',
        on_delete=models.CASCADE, 
        related_name='docs'
    )        
