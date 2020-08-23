# Generated by Django 3.0.7 on 2020-07-10 14:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Zim_Estate_App', '0016_auto_20200710_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 7, 10, 14, 27, 6, 534707, tzinfo=utc), verbose_name='date_posted'),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.CharField(max_length=600),
        ),
    ]
