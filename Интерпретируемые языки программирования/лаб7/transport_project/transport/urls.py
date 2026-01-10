from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/add/', views.trip_add, name='trip_add'),
    path('trip/<int:trip_id>/edit/', views.trip_edit, name='trip_edit'),
]