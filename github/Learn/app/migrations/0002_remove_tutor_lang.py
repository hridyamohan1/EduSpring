# Generated by Django 5.2.1 on 2025-05-28 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='lang',
        ),
    ]
