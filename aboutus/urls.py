from django.urls import path
from . import views

urlpatterns = [
    path('fetch-about-page/', views.about_page_data, name='about_page_data'),
]
