# Generated by Django 4.2.5 on 2023-09-06 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0004_slides_mainbanner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainbanner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال / غیرفعال'),
        ),
    ]
