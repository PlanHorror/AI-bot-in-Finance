# Generated by Django 5.1.3 on 2024-12-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaldata',
            name='result',
            field=models.ImageField(blank=True, null=True, upload_to='result/'),
        ),
    ]
