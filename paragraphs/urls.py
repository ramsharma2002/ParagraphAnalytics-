from django.urls import path
from .views import dashboard_view, search_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('search/', search_view, name='search'),
]
