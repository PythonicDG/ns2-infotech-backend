from django.urls import path
from . import dashboard

urlpatterns = [
    path('session/', dashboard.session),
    path('catalog/', dashboard.catalog),
    path('content/<str:key>/', dashboard.resource),
    path('content/<str:key>/<int:pk>/', dashboard.resource),
]
