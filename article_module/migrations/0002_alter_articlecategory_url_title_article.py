# Generated by Django 4.2 on 2023-08-15 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='url_title',
            field=models.CharField(max_length=300, unique=True, verbose_name='عنوان در لینک'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان مقاله')),
                ('slug', models.SlugField(allow_unicode=True, max_length=300, verbose_name='عنوان در url')),
                ('image', models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')),
                ('short_description', models.CharField(max_length=300, verbose_name='توضیحات کوتاه')),
                ('is_active', models.BooleanField(verbose_name='فعال/غیرفعال')),
                ('text', models.TextField(verbose_name='متن مقاله')),
                ('selected_category', models.ManyToManyField(to='article_module.articlecategory', verbose_name='دسته بندی ها')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
            },
        ),
    ]
