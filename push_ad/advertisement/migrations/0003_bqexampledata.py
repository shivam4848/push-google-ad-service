# Generated by Django 4.1.4 on 2022-12-25 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_remove_advertisement_meta_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='BQExampleData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=250, null=True)),
                ('description', models.TextField()),
                ('phone_number', models.CharField(default=None, max_length=250, null=True)),
            ],
        ),
    ]