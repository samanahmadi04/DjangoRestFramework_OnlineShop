from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('api/footer-boxes/', views.FooterBoxListView.as_view(), name='api-footer-box-list'),
    path('api/footer-links/', views.FooterLinkListView.as_view(), name='api-footer-link-list'),
    path('api/footer-link-values/', views.FooterLinkValueListView.as_view(), name='api-footer-link-list'),
    path('api/site-settings/', views.SiteSettingListView.as_view(), name='api-site-setting-list'),
    path('api/main-banners/', views.MainBannerListView.as_view(), name='api-main-banner-list'),
    path('api/slides/', views.SlidesListView.as_view(), name='api-slides-list'),
    path('api/Suggested-products/', views.SuggestedProductListview.as_view(), name='suggested-products-list'),
]
