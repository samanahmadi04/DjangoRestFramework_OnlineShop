from django.core.validators import URLValidator, EmailValidator
from django.db import models
from django.core.validators import URLValidator
from Product_module.models import ProductParentCategory, ProductCategory


# Create your models here.


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت', validators=[URLValidator()])
    address = models.CharField(max_length=500, verbose_name='آدرس')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='تلفن')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='ایمیل',
                              validators=[EmailValidator()])
    about_us_text = models.TextField(verbose_name='متن درباره ما')
    site_logo = models.ImageField(upload_to='images/logo/', verbose_name='لوگو')
    is_main_setting = models.BooleanField(verbose_name='تنظیم به عنوان تنظیمات')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


class FooterBox(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک', validators=[URLValidator()])
    footerbox = models.ForeignKey(to=FooterBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLinkValue(models.Model):
    value = models.CharField(max_length=200, verbose_name='مقدار عنوان فوتر')
    footerlink = models.ForeignKey(to=FooterLink, on_delete=models.CASCADE, verbose_name='عنوان فوتر')

    class Meta:
        verbose_name = 'مقدار فوتر'
        verbose_name_plural = 'مقدار های فوتر'

    def __str__(self):
        return f'{self.footerlink} - {self.value}'


class MainBanner(models.Model):
    btn_title = models.CharField(max_length=50, verbose_name='عنوان دکمه')
    btn_url = models.URLField(verbose_name='لینک دکمه', validators=[URLValidator()])
    image = models.ImageField(upload_to='images/banner', verbose_name='تصویر', default=None)
    title_category = models.ForeignKey(to=ProductParentCategory, on_delete=models.CASCADE, related_name='title_cat',
                                       null=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'بنر اصلی'
        verbose_name_plural = 'بنر اصلی'

    def __str__(self):
        return f'{self.btn_title} - {self.title_category}'


class Slides(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    text = models.TextField(null=True, verbose_name='متن')
    btn_title = models.CharField(max_length=50, verbose_name='عنوان دکمه')
    btn_url = models.URLField(verbose_name='لینک دکمه', validators=[URLValidator()])
    slide_url = models.URLField(verbose_name='لینک اسلاید', validators=[URLValidator()])
    image = models.ImageField(upload_to='images/slides', verbose_name='تصویر')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدها'

    def __str__(self):
        return f'{self.title} - {self.btn_title}'


class SuggestedProductSection(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='دسته بندی')
    parent_category = models.ForeignKey(to=ProductParentCategory, on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='دسته بندی والد')
    image = models.ImageField(upload_to='images/suggustion', verbose_name='تصویر')

    def __str__(self):
        return f'{self.title}-{self.category}'

    class Meta:
        verbose_name = 'محصول پیشنهادی'
        verbose_name_plural = 'محصولات پیشنهادی'
