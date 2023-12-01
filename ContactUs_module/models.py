from django.db import models
from django.core.validators import URLValidator, EmailValidator


# Create your models here.


class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='نام')
    last_name = models.CharField(max_length=30, verbose_name='نام خانوداگی')
    email = models.EmailField(max_length=250, validators=[EmailValidator], verbose_name='ایمیل')
    phone = models.CharField(max_length=20, verbose_name='شماره تلفن')
    message = models.TextField(verbose_name='پیام')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return f'{self.first_name} - {self.email}'
