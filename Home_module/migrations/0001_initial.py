# Generated by Django 4.2.5 on 2023-09-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100, verbose_name='نام سایت')),
                ('site_url', models.CharField(max_length=200, verbose_name='دامنه سایت')),
                ('address', models.CharField(max_length=500, verbose_name='آدرس')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='تلفن')),
                ('email', models.EmailField(blank=True, max_length=150, null=True, verbose_name='ایمیل')),
                ('about_us_text', models.TextField(verbose_name='متن درباره ما')),
                ('site_logo', models.ImageField(upload_to='images/logo/', verbose_name='لوگو')),
                ('is_main_setting', models.BooleanField(verbose_name='تنظیم به عنوان تنظیمات')),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات',
            },
        ),
    ]