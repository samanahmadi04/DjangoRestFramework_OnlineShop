from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('api/products/', views.ProductsListView.as_view()),
    path('api/products/<str:category>/', views.ProductsListView.as_view()),
    path('api/product-parent-categories/', views.ProductParentCategoryListView.as_view()),
    path('api/product-categories/', views.ProductCategoryListView.as_view()),
    path('api/product-options/', views.ProdictOptionListView.as_view()),
    path('api/product-options-value/', views.ProdictOptionValueListView.as_view()),
]
