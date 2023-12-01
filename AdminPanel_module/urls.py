from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'AdminPanel_module'

urlpatterns = [
    #PRODUCTS
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductList.as_view()),
    #PARENT-CATEGORIES
    path('parent-categories/', views.ParentCategoryList.as_view()),
    path('parent-categories/<int:pk>/', views.ParentCategoryList.as_view()),
    #CATEGORIES
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryList.as_view()),
    #OPTION-FIELDS
    path('option-fields/', views.OptionFieldList.as_view()),
    path('option-fields/<int:pk>/', views.OptionFieldList.as_view()),
    #PRODUCT-OPTIONS
    path('product-options/', views.ProductOptionList.as_view()),
    path('product-options/<int:pk>/', views.ProductOptionList.as_view()),
    #SITE-SETTINGS
    path('site-settings/', views.SiteSettingList.as_view()),
    path('site-settings/<int:pk>/', views.SiteSettingList.as_view()),
    #FOOTER-BOXES
    path('footer-boxes/', views.FooterBoxList.as_view()),
    path('footer-boxes/<int:pk>/', views.FooterBoxList.as_view()),  # ta akhar inja check shode!!
    #FOOTER-LINKES
    path('footer-links/', views.FooterLinkList.as_view()),
    path('footer-links/<int:pk>/', views.FooterLinkList.as_view()),
    path('footer-link-values/', views.FooterLinkValueList.as_view()),
    path('footer-link-values/<int:pk>/', views.FooterLinkValueList.as_view()),
    #MAIN-BANNERS
    path('main-banners/', views.MainBannerList.as_view()),
    path('main-banners/<int:pk>/', views.MainBannerList.as_view()),
    #SLIDES
    path('slides/', views.SlidesList.as_view()),
    path('slides/<int:pk>/', views.SlidesList.as_view()),
    #CONTACT
    path('contacts/', views.ContactSubmissionList.as_view()),
    path('contacts/<int:pk>/', views.ContactSubmissionList.as_view()),
    # OBTAIN AUTH TOKEN
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]
