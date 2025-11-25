# ocr_app/urls.py (MODIFIED)

from django.urls import path
from . import views

urlpatterns = [
    # 🌟 ADD THIS LINE: Maps the base path to the status_check view
    path('status_check/', views.status_check, name='status_check'), 
    
    # Existing API Endpoints
    path('process_image/', views.process_image, name='process_image'),
    path('records/', views.get_records, name='get_records'),
    path('clear_records/', views.clear_records, name='clear_records'),
]