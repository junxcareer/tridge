# Generated by Django 4.0.1 on 2022-01-14 15:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_choice_approved_alter_question_closed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='max_choices',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='question',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 21, 15, 54, 23, 93922, tzinfo=utc), verbose_name='date closed'),
        ),
    ]
