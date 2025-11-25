# ocr_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Site
    path('admin/', admin.site.urls),
    
    # 2. Key Fix: Include all paths from your app starting at the root ('')
    path('', include('ocr_app.urls')), 
    
    # 3. Media Files (for development)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)