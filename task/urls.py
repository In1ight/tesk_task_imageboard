from django.urls import path
from . import views


app_name = 'test_task'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:idd>/view/', views.post_detail, name='post_detail'),
    path('<int:idd>/edit/', views.post_edit, name='post_edit'),
    path('add/', views.post_add, name='post_add'),
]