# Generated by Django 3.1.1 on 2020-10-06 21:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201007_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]