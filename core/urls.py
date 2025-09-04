from django.urls import path
from .views import HeaderFooterAPIView
from .views import *

urlpatterns = [
    path('header-footer/', HeaderFooterAPIView.as_view(), name='header-footer'),
    path('contact/', contact_form_submit, name='contact-form-submit'),
]
