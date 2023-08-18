from django.urls import path

from . import views

urlpatterns = [
    path('a-rack/', views.a_rack, name='a_rack'),
    path('a-rack/palette/detail/<int:pk>/', views.palette_detail, name='palette_detail'),
    path('a-rack/palette/edit/<int:pk>/', views.palette_edit, name='palette_edit'),
    path('a-rack/palette/sheet/add/<int:pk>/', views.add_sheet_to_palette, name='add_sheet_to_palette'),
    path('a-rack/palette/sheet/delete/<int:pk>/', views.sheet_on_palette_delete, name='sheet_on_palette_delete'),
]
