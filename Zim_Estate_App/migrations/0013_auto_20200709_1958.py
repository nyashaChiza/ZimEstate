# Generated by Django 3.0.7 on 2020-07-09 17:58

import datetime
import django.core.files.storage
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Zim_Estate_App', '0012_auto_20200709_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 7, 9, 17, 58, 33, 847087, tzinfo=utc), verbose_name='date_posted'),
        ),
        migrations.AlterField(
            model_name='property',
            name='image1',
            field=models.ImageField(null=True, upload_to=django.core.files.storage.FileSystemStorage(location='static/Zim_Estate_App/posts')),
        ),
        migrations.AlterField(
            model_name='property',
            name='image2',
            field=models.ImageField(null=True, upload_to=django.core.files.storage.FileSystemStorage(location='static/Zim_Estate_App/posts')),
        ),
        migrations.AlterField(
            model_name='property',
            name='image3',
            field=models.ImageField(null=True, upload_to=django.core.files.storage.FileSystemStorage(location='static/Zim_Estate_App/posts')),
        ),
    ]
