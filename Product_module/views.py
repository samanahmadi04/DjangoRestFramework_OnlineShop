from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, ProductParentCategory, ProductCategory, ProductOption, OptionField
from .serializers import ProductSerializer, ProductParentCategorySerializer, ProductCategorySerializer, \
    ProductOptionSerializer, OptionFieldSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage


class ProductsListView(APIView):
    """
    لیست محصولات و فیلترینگ
    """

    def get(self, request):
        category = request.GET.get('category')
        search_query = request.GET.get('q')

        # Start with all products
        products = Product.objects.all()

        # Apply filters based on 'category' and 'q' parameters
        if category:
            products = products.filter(
                Q(category__title__icontains=category) | Q(category__parent_category__title__icontains=category)
            )

        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Create a Paginator instance with 6 products per page
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')  # Get the page number from the request query parameters

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            # Handle the case where the page number is out of range
            page = paginator.page(1)  # Default to the first page

        serializer = ProductSerializer(instance=page, many=True)
        return Response({
            'page_number': page_number,
            'total_pages': paginator.num_pages,
            'products': serializer.data
        })


class ProductParentCategoryListView(APIView):
    """
    لیست دسته بندی های اصلی
    """

    def get(self, request):
        productparents = ProductParentCategory.objects.all()
        ser_data = ProductParentCategorySerializer(instance=productparents, many=True)
        return Response(ser_data.data)


class ProductCategoryListView(APIView):
    """
    لیست دسته بندی ها
    """

    def get(self, request):
        productcategories = ProductCategory.objects.all()
        ser_data = ProductCategorySerializer(instance=productcategories, many=True)
        return Response(ser_data.data)


class ProdictOptionListView(APIView):
    """
    لیست ویژگی های محصول
    """

    def get(self, request):
        productoption = OptionField.objects.all()
        ser_data = OptionFieldSerializer(instance=productoption, many=True)
        return Response(ser_data.data)


class ProdictOptionValueListView(APIView):
    """
    لیست مقادیر ویژگی های محصول
    """

    def get(self, request):
        productoption = ProductOption.objects.all()
        ser_data = ProductOptionSerializer(instance=productoption, many=True)
        return Response(ser_data.data)
