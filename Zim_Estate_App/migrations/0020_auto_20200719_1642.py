# Generated by Django 3.0.7 on 2020-07-19 14:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Zim_Estate_App', '0019_auto_20200710_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='posted_on_facebook',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 7, 19, 14, 41, 57, 622282, tzinfo=utc), verbose_name='date_posted'),
        ),
    ]