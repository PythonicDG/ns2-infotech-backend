from django.urls import path
from .views import PortfolioSectionsAPIView

urlpatterns = [
    path('fetch-portfolio/', PortfolioSectionsAPIView.as_view(), name = 'page-sections'),
]
