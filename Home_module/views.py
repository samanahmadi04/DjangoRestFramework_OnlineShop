from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FooterBox, FooterLink, SiteSetting, MainBanner, Slides, FooterLinkValue, SuggestedProductSection
from .serializers import FooterBoxSerializer, FooterLinkSerializer, SiteSettingSerializer, MainBannerSerializer, \
    SlidesSerializer, FooterLinkValueSerializer, SuggestedProductSectionSerializer


# Create your views here.

class FooterBoxListView(APIView):
    """
    لیست عناوین لینک‌های فوتر
    """

    def get(self, request):
        footer_boxes = FooterBox.objects.all()
        serializer = FooterBoxSerializer(footer_boxes, many=True)
        return Response(serializer.data)


class FooterLinkListView(APIView):
    """
    لیست لینک‌های فوتر
    """

    def get(self, request):
        footer_links = FooterLink.objects.all()
        serializer = FooterLinkSerializer(footer_links, many=True)
        return Response(serializer.data)


class FooterLinkValueListView(APIView):
    """
    لیست مقدار های لینک‌های فوتر
    """

    def get(self, request):
        footer_link_values = FooterLinkValue.objects.all()
        serializer = FooterLinkValueSerializer(footer_link_values, many=True)
        return Response(serializer.data)


class SiteSettingListView(APIView):
    """
    لیست تنظیمات سایت
    """

    def get(self, request):
        site_settings = SiteSetting.objects.all()
        serializer = SiteSettingSerializer(site_settings, many=True)
        return Response(serializer.data)


class MainBannerListView(APIView):
    """
    لیست بنر بزرگ بالای سایت
    """

    def get(self, request):
        site_settings = MainBanner.objects.all()
        serializer = MainBannerSerializer(site_settings, many=True)
        return Response(serializer.data)


class SlidesListView(APIView):
    """
    لیست بنر‌های کوچیک پایین بنر اصلی
    """

    def get(self, request):
        site_settings = Slides.objects.all()
        serializer = SlidesSerializer(site_settings, many=True)
        return Response(serializer.data)


class SuggestedProductListview(APIView):
    """
    محصولات پیشنهادی در اسلایدر های پایین سایت
    """

    def get(self, request):
        SuggustedProducts = SuggestedProductSection.objects.all()
        serializer = SuggestedProductSectionSerializer(instance=SuggustedProducts, many=True)
        return Response(serializer.data)
