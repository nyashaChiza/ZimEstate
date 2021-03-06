# Generated by Django 3.0.7 on 2020-07-10 12:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Zim_Estate_App', '0013_auto_20200709_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 12, 31, 9, 920176, tzinfo=utc), verbose_name='date_posted'),
        ),
        migrations.AlterField(
            model_name='property',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='property',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='property',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
