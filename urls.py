from django.urls import path
from . import views
from .views import LoginView, RegisterView
from django.urls import include, path
app_name = 'dataapp'

urlpatterns = [
    
    path('upload/', views.upload_file, name='upload_file'),
    path('file_list/', views.file_list, name='file_list'),
    path('visualize/<int:file_id>/', views.visualize_data, name='visualize_data'),
    path('', views.upload_file, name='upload_file'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
     path('files/<int:file_id>/', views.file_list, name='file_list'),
    
]
