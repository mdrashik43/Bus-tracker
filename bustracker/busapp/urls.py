from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.student_map, name='student_map'),
    path('supervisor/', views.supervisor_panel, name='supervisor_panel'),
    path('api/buses/', views.api_buses, name='api_buses'),
]