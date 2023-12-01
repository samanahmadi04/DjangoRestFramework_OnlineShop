from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ContactUs_module.models import ContactSubmission
from ContactUs_module.serializers import ContactSubmissionSerializer
from Home_module.models import SiteSetting, FooterBox, FooterLink, FooterLinkValue, MainBanner, Slides
from Home_module.serializers import SiteSettingSerializer, FooterBoxSerializer, FooterLinkSerializer, \
    FooterLinkValueSerializer, MainBannerSerializer, SlidesSerializer
from Product_module.models import Product, ProductParentCategory, ProductCategory, OptionField, ProductOption
from rest_framework import status
from Product_module.serializers import ProductSerializer, ProductParentCategorySerializer, ProductCategorySerializer, \
    OptionFieldSerializer, ProductOptionSerializer
from django.core.paginator import Paginator, EmptyPage


# Create your views here.

# PRODUCT_MODULE

class ProductList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)
        serializer = ProductSerializer(instance=page, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data['title']

        # Check if a Product with the same title already exists
        existing_product = Product.objects.filter(title=title).first()

        if existing_product:
            # Update the existing Product instead of creating a new one
            existing_product.category.set(data.get('category', []))
            existing_product.price = data.get('price', existing_product.price)
            existing_product.description = data.get('description', existing_product.description)
            existing_product.image = data.get('image', existing_product.image)
            existing_product.active = data.get('active', existing_product.active)
            existing_product.deleted = data.get('deleted', existing_product.deleted)
            existing_product.save()
        else:
            # Create a new Product if it doesn't exist
            new_product = Product.objects.create(title=title)
            new_product.category.set(data.get('category', []))
            new_product.price = data.get('price', new_product.price)
            new_product.description = data.get('description', new_product.description)
            new_product.image = data.get('image', new_product.image)
            new_product.active = data.get('active', new_product.active)
            new_product.deleted = data.get('deleted', new_product.deleted)
            new_product.save()

        serializer = ProductSerializer(existing_product if existing_product else new_product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        if pk is not None:
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            product.title = data.get('title', product.title)
            product.category.set(data.get('category', product.category.all()))
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            product.image = data.get('image', product.image)
            product.active = data.get('active', product.active)
            product.deleted = data.get('deleted', product.deleted)
            product.save()

            serializer = ProductSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "To update a product, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is not None:
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            product.title = data.get('title', product.title)
            product.category.set(data.get('category', product.category.all()))
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            product.image = data.get('image', product.image)
            product.active = data.get('active', product.active)
            product.deleted = data.get('deleted', product.deleted)
            product.save()

            serializer = ProductSerializer(product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "To update a product, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParentCategoryList(APIView):
    def get(self, request):
        parentcategories = ProductParentCategory.objects.all()
        serializer = ProductParentCategorySerializer(instance=parentcategories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductParentCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        parentcategory = get_object_or_404(ProductParentCategory, pk=pk)
        serializer = ProductParentCategorySerializer(parentcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        parentcategory = get_object_or_404(ProductParentCategory, pk=pk)
        serializer = ProductParentCategorySerializer(parentcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        parentcategory = get_object_or_404(ProductParentCategory, pk=pk)
        parentcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(instance=categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')

        # Check if a ProductCategory with the same title already exists
        existing_category = ProductCategory.objects.filter(title=title).first()

        if existing_category:
            # Update the existing ProductCategory instead of creating a new one
            existing_category.parent_category.set(data.get('parent_category', []))
            existing_category.save()
        else:
            # Create a new ProductCategory if it doesn't exist
            new_category = ProductCategory.objects.create(title=title)
            new_category.parent_category.set(data.get('parent_category', []))
            new_category.save()

        # Handle 'parent_category' here if it exists in the data

        serializer = ProductCategorySerializer(existing_category if existing_category else new_category)

        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(ProductCategory, pk=pk)
        serializer = ProductCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the many-to-many field 'parent_category' if it exists in the request data
            parent_category_data = request.data.get('parent_category')
            if parent_category_data is not None:
                category.parent_category.set(parent_category_data)
                category.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        category = get_object_or_404(ProductCategory, pk=pk)
        serializer = ProductCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update the many-to-many field 'parent_category' if it exists in the request data
            parent_category_data = request.data.get('parent_category')
            if parent_category_data is not None:
                category.parent_category.set(parent_category_data)
                category.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(ProductCategory, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OptionFieldList(APIView):
    def get(self, request):
        optionfields = OptionField.objects.all()
        serializer = OptionFieldSerializer(instance=optionfields, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')

        # Check if an OptionField with the same title already exists
        existing_optionfield = OptionField.objects.filter(title=title).first()

        if existing_optionfield:
            # Update the existing OptionField instead of creating a new one
            existing_optionfield.category.set(data.get('category', []))
            existing_optionfield.save()
        else:
            # Create a new OptionField if it doesn't exist
            new_optionfield = OptionField.objects.create(title=title)
            new_optionfield.category.set(data.get('category', []))
            new_optionfield.save()

        # Handle 'optionfield' here if it exists in the data

        serializer = OptionFieldSerializer(existing_optionfield if existing_optionfield else new_optionfield)

        return Response(serializer.data)

    def put(self, request, pk):
        optionfield = get_object_or_404(OptionField, pk=pk)
        serializer = OptionFieldSerializer(optionfield, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the many-to-many field 'category' if it exists in the request data
            category_data = request.data.get('category')
            if category_data is not None:
                optionfield.category.set(category_data)
                optionfield.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        optionfield = get_object_or_404(OptionField, pk=pk)
        serializer = OptionFieldSerializer(optionfield, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update the many-to-many field 'category' if it exists in the request data
            category_data = request.data.get('category')
            if category_data is not None:
                optionfield.category.set(category_data)
                optionfield.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            optionfield = OptionField.objects.get(id=pk)
        except OptionField.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        optionfield.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductOptionList(APIView):
    def get(self, request):
        productoptions = ProductOption.objects.all()
        serializer = ProductOptionSerializer(instance=productoptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductOptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if pk:
            try:
                productoption = ProductOption.objects.get(id=pk)
            except ProductOption.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ProductOptionSerializer(instance=productoption, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a product option, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk:
            try:
                productoption = ProductOption.objects.get(id=pk)
            except ProductOption.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ProductOptionSerializer(productoption, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a product option, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            productoption = ProductOption.objects.get(id=pk)
        except ProductOption.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        productoption.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# END OF PRODUCT MODULE

# HOME_MODULE

class SiteSettingList(APIView):
    def get(self, request):
        site_settings = SiteSetting.objects.all()
        serializer = SiteSettingSerializer(instance=site_settings, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SiteSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        site_setting = get_object_or_404(SiteSetting, pk=pk)
        serializer = SiteSettingSerializer(site_setting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        site_setting = get_object_or_404(SiteSetting, pk=pk)
        serializer = SiteSettingSerializer(site_setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        site_setting = get_object_or_404(SiteSetting, pk=pk)
        site_setting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FooterBoxList(APIView):
    def get(self, request):
        footer_boxes = FooterBox.objects.all()
        serializer = FooterBoxSerializer(instance=footer_boxes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = FooterBoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        footer_box = get_object_or_404(FooterBox, pk=pk)
        serializer = FooterBoxSerializer(footer_box, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        footer_box = get_object_or_404(FooterBox, pk=pk)
        serializer = FooterBoxSerializer(footer_box, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        footer_box = get_object_or_404(FooterBox, pk=pk)
        footer_box.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FooterLinkList(APIView):
    def get(self, request):
        footer_links = FooterLink.objects.all()
        serializer = FooterLinkSerializer(instance=footer_links, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FooterLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        footer_link = get_object_or_404(FooterLink, pk=pk)
        serializer = FooterLinkSerializer(footer_link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        footer_link = get_object_or_404(FooterLink, pk=pk)
        serializer = FooterLinkSerializer(footer_link, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        footer_link = get_object_or_404(FooterLink, pk=pk)
        footer_link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FooterLinkValueList(APIView):
    def get(self, request):
        footer_link_values = FooterLinkValue.objects.all()
        serializer = FooterLinkValueSerializer(instance=footer_link_values, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FooterLinkValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        footer_link_value = get_object_or_404(FooterLinkValue, pk=pk)
        serializer = FooterLinkValueSerializer(footer_link_value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        footer_link_value = get_object_or_404(FooterLinkValue, pk=pk)
        serializer = FooterLinkValueSerializer(footer_link_value, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        footer_link_value = get_object_or_404(FooterLinkValue, pk=pk)
        footer_link_value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MainBannerList(APIView):
    def get(self, request):
        mainbanners = MainBanner.objects.all()
        serializer = MainBannerSerializer(instance=mainbanners, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MainBannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if pk:
            try:
                mainbanner = MainBanner.objects.get(id=pk)
            except MainBanner.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = MainBannerSerializer(instance=mainbanner, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a main banner, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk:
            try:
                mainbanner = MainBanner.objects.get(id=pk)
            except MainBanner.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = MainBannerSerializer(mainbanner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a main banner, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            mainbanner = MainBanner.objects.get(id=pk)
        except MainBanner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        mainbanner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlidesList(APIView):
    def get(self, request):
        slides = Slides.objects.all()
        serializer = SlidesSerializer(instance=slides, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SlidesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if pk:
            try:
                slide = Slides.objects.get(id=pk)
            except Slides.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = SlidesSerializer(instance=slide, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a slide, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk:
            try:
                slide = Slides.objects.get(id=pk)
            except Slides.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = SlidesSerializer(slide, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a slide, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            slide = Slides.objects.get(id=pk)
        except Slides.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        slide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# END OF HOME_MODULE

# CONTACTUS_MODULE

class ContactSubmissionList(APIView):
    def get(self, request):
        contacts = ContactSubmission.objects.all()
        serializer = ContactSubmissionSerializer(instance=contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is not None:
            try:
                contact = ContactSubmission.objects.get(id=pk)
            except ContactSubmission.DoesNotExist:
                return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContactSubmissionSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a contact, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk is not None:
            try:
                contact = ContactSubmission.objects.get(id=pk)
            except ContactSubmission.DoesNotExist:
                return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContactSubmissionSerializer(contact, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "To update a contact, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            try:
                contact = ContactSubmission.objects.get(id=pk)
            except ContactSubmission.DoesNotExist:
                return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)

            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "To delete a contact, provide a valid 'pk' in the URL."},
                        status=status.HTTP_400_BAD_REQUEST)

# END OF CONTACTUS_MODULE
