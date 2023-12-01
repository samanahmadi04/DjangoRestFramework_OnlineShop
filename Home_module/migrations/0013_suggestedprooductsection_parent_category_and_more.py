# Generated by Django 4.2.5 on 2023-09-20 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product_module', '0013_product_purchase_guide_alter_product_price'),
        ('Home_module', '0012_suggestedprooductsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestedprooductsection',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product_module.productparentcategory', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='suggestedprooductsection',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product_module.productcategory', verbose_name='دسته بندی'),
        ),
    ]
