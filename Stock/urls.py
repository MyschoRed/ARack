from django.urls import path

from . import views

urlpatterns = [
    path('stock/', views.stock, name='stock'),
    path('stock-status/', views.stock_status, name='stock_status'),
    path('stock-status/edit/<int:pk>/', views.stock_palette_edit, name='stock_palette_edit'),
]
