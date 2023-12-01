from rest_framework import serializers
from .models import Product, ProductParentCategory, ProductCategory, ProductOption, OptionField


class ProductParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParentCategory
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.SerializerMethodField()

    def get_parent_category(self, obj):
        parent_categories = obj.parent_category.all()
        return [parent_category.title for parent_category in parent_categories]

    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    id = serializers.IntegerField(read_only=True)
    categories = serializers.SerializerMethodField()
    Purchase_guide = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField()
    description = serializers.CharField()

    def get_categories(self, obj):
        categories = obj.category.all()
        return [category.title for category in categories]


class OptionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionField
        fields = '__all__'


class ProductOptionSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = ProductOption
        fields = '__all__'

    def get_product_title(self, obj):
        return obj.product.title if obj.product else None

    def get_product_id(self, obj):
        return obj.product.id if obj.product else None
