# Generated by Django 4.2 on 2024-05-31 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0012_productgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.ImageField(upload_to='product_gallery', verbose_name='تصویر گالری'),
        ),
    ]
