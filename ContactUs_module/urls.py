from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactSubmissionView.as_view(), name='contact-us')
]
