# Generated by Django 4.1.4 on 2022-12-24 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='meta_data',
        ),
    ]
