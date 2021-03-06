# Generated by Django 4.0.1 on 2022-01-14 15:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_remove_question_is_closed_question_closed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 21, 15, 41, 59, 767156, tzinfo=utc), verbose_name='date closed'),
        ),
    ]
