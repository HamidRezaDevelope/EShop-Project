# Generated by Django 4.2 on 2024-01-17 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0004_contactus_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
