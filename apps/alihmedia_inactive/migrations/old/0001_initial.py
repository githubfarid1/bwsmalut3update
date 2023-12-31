# Generated by Django 4.2.3 on 2023-08-11 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('box_number', models.SmallIntegerField()),
                ('bundle_number', models.SmallIntegerField()),
                ('code', models.CharField(max_length=20)),
                ('title', models.TextField()),
                ('year', models.CharField(max_length=4)),
                ('orinot', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('defcode', models.CharField(max_length=20, unique=True)),
                ('link', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('doc_number', models.SmallIntegerField()),
                ('doc_count', models.SmallIntegerField()),
                ('orinot', models.CharField(max_length=10)),
                ('doc_type', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('filesize', models.IntegerField()),
                ('page_count', models.SmallIntegerField()),
                ('bundle', models.ForeignKey(db_column='bundle_id', on_delete=django.db.models.deletion.CASCADE, related_name='docs', to='alihmedia_inactive.bundle')),
            ],
        ),
        migrations.AddField(
            model_name='bundle',
            name='department',
            field=models.ForeignKey(db_column='department_id', on_delete=django.db.models.deletion.CASCADE, related_name='bundles', to='alihmedia_inactive.department'),
        ),
    ]
