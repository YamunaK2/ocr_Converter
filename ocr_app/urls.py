# ocr_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This path maps the base URL (http://10.136.90.160:8000/) to the status_check view.
    path('', views.status_check, name='status_check'), 
    
    # Other API Endpoints
    path('process_image/', views.process_image, name='process_image'),
    path('records/', views.get_records, name='get_records'),
    path('clear_records/', views.clear_records, name='clear_records'),
]