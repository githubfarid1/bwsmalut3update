# Generated by Django 4.2.3 on 2023-11-08 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fm_pjpa', '0008_department_create_date_subfolder_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subfolder',
            name='folder',
            field=models.CharField(max_length=50),
        ),
    ]
