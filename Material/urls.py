from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('material/sheet-list/', views.sheet_list, name='sheet_list'),
    path('material/sheet-add/', views.sheet_add, name='sheet_add'),
    path('material/sheet-detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('material/sheet-edit/<int:pk>/', views.sheet_edit, name='sheet_edit'),
    path('material/sheet-delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),
]
