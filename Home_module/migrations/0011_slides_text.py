# Generated by Django 4.2.5 on 2023-09-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_module', '0010_remove_slides_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='slides',
            name='text',
            field=models.TextField(null=True, verbose_name='متن'),
        ),
    ]
