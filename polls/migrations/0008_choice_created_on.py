# Generated by Django 4.0.1 on 2022-01-14 13:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]