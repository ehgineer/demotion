from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('page1/', views.upload_image, name='upload_image'),
    path('page2/<int:pred_id>', views.show_result, name='show_result')
]