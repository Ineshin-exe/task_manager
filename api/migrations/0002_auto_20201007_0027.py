# Generated by Django 3.1.1 on 2020-10-06 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='createdAt',
            field=models.DateTimeField(null=True),
        ),
    ]
