from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('a-rack/', views.a_rack, name='a_rack'),

    # path('palettes-list/', views.palette_list, name='paletts_list'),
    path('palette/detail/<int:pk>/', views.palette_detail, name='palette_detail'),
    path('palette/edit/<int:pk>/', views.palette_edit, name='palette_edit'),
    path('palette/sheet/add/<int:pk>/', views.add_sheet_to_palette, name='add_sheet_to_palette'),
    path('palette/sheet/delete/<int:pk>/', views.sheet_on_palette_delete, name='sheet_on_palette_delete'),

    path('sheet-list/', views.sheet_list, name='sheet_list'),
    path('sheet-add/', views.sheet_add, name='sheet_add'),
    path('sheet-detail/<int:pk>/', views.sheet_detail, name='sheet_detail'),
    path('sheet-edit/<int:pk>/', views.sheet_edit, name='sheet_edit'),
    path('sheet-delete/<int:pk>/', views.sheet_delete, name='sheet_delete'),

    path('material-issue-list/', views.material_issue_list, name='material_issue_list'),

    path('stock-status/', views.stock_status, name='stock_status'),

    path('stock/', views.stock, name='stock'),

    path('login/', auth_views.LoginView.as_view(template_name='Core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration, name='registration'),

]
