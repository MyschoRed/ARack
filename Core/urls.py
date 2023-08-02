from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('a-rack/', views.a_rack, name='a_rack'),
    path('palette/detail/<int:pk>/', views.palette_detail, name='palette_detail'),
    path('palette/edit/<int:pk>/', views.palette_edit, name='palette_edit'),
    path('palettes-list/', views.palette_list, name='paletts_list'),
    path('palette/sheet/add/<int:pk>/', views.add_sheet_to_palette, name='add_sheet_to_palette'),
    path('palette/sheet/delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),
    path('sheet-list/', views.sheet_list, name='sheet_list'),

    path('stock/', views.stock, name='stock'),

    path('login/', auth_views.LoginView.as_view(template_name='Core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration, name='registration'),
]
