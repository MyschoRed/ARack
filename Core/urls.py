from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('palette/detail/<int:pk>/', views.palette_detail, name='palette_detail'),
    path('palette/edit/<int:pk>/', views.palette_edit, name='palette_edit'),
    path('palettes-list/', views.palette_list, name='paletts_list'),
    path('palette/sheet/add/<int:pk>/', views.add_sheet_to_palette, name='add_sheet_to_palette'),
    path('palette/sheet/delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),

    path('sheet-list/', views.sheet_list, name='sheet_list'),

]