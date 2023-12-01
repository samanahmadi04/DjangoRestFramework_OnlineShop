from rest_framework import serializers

from Product_module.models import ProductCategory
from .models import FooterLink, FooterBox, SiteSetting, MainBanner, Slides, FooterLinkValue, SuggestedProductSection


class FooterLinkSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    url = serializers.URLField(max_length=500)
    footerbox = serializers.SerializerMethodField(method_name='get_footerbox')

    def get_footerbox(self, obj):
        footerboxes = FooterBox.objects.filter(footerlink=obj)
        return [footerbox.title for footerbox in footerboxes]


class FooterLinkValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLinkValue
        fields = '__all__'


class FooterBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterBox
        fields = "__all__"


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = "__all__"


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = "__all__"


class SlidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slides
        fields = "__all__"


class SuggestedProductSectionSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()
    parent_category_title = serializers.SerializerMethodField()

    def get_category_title(self, obj):
        if obj.category:
            return obj.category.title
        else:
            return None

    def get_parent_category_title(self, obj):
        if obj.parent_category:
            return obj.parent_category.title
        else:
            return None

    class Meta:
        model = SuggestedProductSection
        fields = ["id", "title", "image", "category_title", "parent_category_title"]
