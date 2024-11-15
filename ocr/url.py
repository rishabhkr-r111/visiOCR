from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('process_image/', views.process_image, name='process_image'),
  path('verify/', views.verify, name='verify'),
  path('verify_id/', views.verify_id, name='verify_id'),
]