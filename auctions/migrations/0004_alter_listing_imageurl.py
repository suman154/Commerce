# Generated by Django 5.0.4 on 2024-05-13 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.CharField(max_length=10000),
        ),
    ]
