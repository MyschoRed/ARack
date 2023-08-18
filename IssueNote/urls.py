from django.urls import path

from . import views

urlpatterns = [
    path('issue-note-list/', views.material_issue_list, name='issue_note_list'),
]
