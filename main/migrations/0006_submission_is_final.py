# Generated by Django 2.1.5 on 2019-02-06 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_contest_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='is_final',
            field=models.BooleanField(default=False),
        ),
    ]