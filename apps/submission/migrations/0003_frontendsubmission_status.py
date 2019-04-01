# Generated by Django 2.1.5 on 2019-03-27 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20190326_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontendsubmission',
            name='status',
            field=models.CharField(choices=[('PN', 'Pending'), ('OK', 'Ok'), ('ER', 'Error')], default='PN', max_length=2),
        ),
    ]