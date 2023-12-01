from django.db import models
from django.db import models
# Create your models here.
from django.utils.text import slugify


class ProductParentCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی اصلی'
        verbose_name_plural = 'دسته بندی های اصلی'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    parent_category = models.ManyToManyField(to=ProductParentCategory, db_index=True, related_name="parentcategory")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    id = models.AutoField(primary_key=True)
    category = models.ManyToManyField(to=ProductCategory, related_name='category', db_index=True,
                                      verbose_name='دسته بندی')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='قیمت')
    description = models.TextField(verbose_name='توضیحات محصول')
    purchase_guide = models.TextField(default='برای اطلاعات بیشتر تماس بگیرید', verbose_name='روش خرید')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')

    def save(self, *args, **kwargs):
        # Regenerate the slug only if the title has changed or if it's a new product.
        if not self.id or not Product.objects.filter(id=self.id).exists() or self.title != Product.objects.get(
                id=self.id).title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.price}"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class OptionField(models.Model):
    title = models.CharField(max_length=20, unique=True, verbose_name='عنوان ویژگی')
    category = models.ManyToManyField(ProductParentCategory, null=True,
                                      verbose_name='دسته بندی مربوطه')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'عنوان ویژگی'
        verbose_name_plural = 'عنوان ویژگی ها'


class ProductOption(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='محصول')
    option_field = models.ForeignKey(to=OptionField, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='option_field', verbose_name='عنوان ویژگی')

    value = models.CharField(max_length=20, null=True, blank=True, verbose_name='مقدار ویژگی')

    def __str__(self):
        return f'{self.product} - {self.option_field}: {self.value}'

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'
