# Generated by Django 2.1.7 on 2019-03-19 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_auto_20190319_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='phno',
        ),
    ]