# Generated by Django 3.0.3 on 2020-07-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_entry_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='result',
            field=models.ImageField(upload_to='predict/'),
        ),
    ]
