# Generated by Django 3.0.3 on 2020-07-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0004_auto_20200725_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='result',
            field=models.ImageField(blank=True, upload_to='predict/'),
        ),
    ]
