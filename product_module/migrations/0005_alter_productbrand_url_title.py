# Generated by Django 4.2 on 2024-03-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_productbrand_url_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbrand',
            name='url_title',
            field=models.CharField(default='url_title', max_length=100, verbose_name='عنوان در url'),
            preserve_default=False,
        ),
    ]
