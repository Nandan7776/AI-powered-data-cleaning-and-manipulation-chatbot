from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('clean_data/', views.clean_data, name='data_cleaning'),
    path('download_cleaned_data/', views.download_cleaned_data, name='download_cleaned_data'),
    path('instructions/', views.instructions, name='instructions'),
]