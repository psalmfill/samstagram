# Generated by Django 3.2.11 on 2022-01-16 07:02

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_path_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(max_length=255, upload_to=core.models.scramble_uploaded_filename),
        ),
    ]