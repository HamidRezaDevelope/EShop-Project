# Generated by Django 4.2 on 2023-08-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_user',
            field=models.TextField(blank=True, null=True, verbose_name='درباره شخص'),
        ),
    ]
