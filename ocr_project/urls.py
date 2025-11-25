# ocr_project/urls.py

from django.contrib import admin
from django.urls import path, include

# Import the necessary modules for serving media files
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ocr_app.urls')),
]

# ⚠️ IMPORTANT: Only serve media files this way in DEVELOPMENT (when DEBUG=True)
# For production, you must use a proper web server (like Nginx or Apache).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)