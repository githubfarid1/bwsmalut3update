# Generated by Django 4.2.3 on 2023-11-09 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fm_pjpa', '0009_alter_subfolder_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
