from django.urls import path
from .views import HeaderFooterAPIView

urlpatterns = [
    path('header-footer/', HeaderFooterAPIView.as_view(), name='header-footer'),
]
