# ocr_app/admin.py

from django.contrib import admin
from .models import OcrRecord

# 1. Define how the model should look in the Admin interface
class OcrRecordAdmin(admin.ModelAdmin):
    # Fields displayed in the list view (list_display)
    list_display = (
        'id', 
        'filename', 
        'status', 
        'file_size', 
        'created_at'
    )
    
    # Fields that can be filtered on the right sidebar (list_filter)
    list_filter = ('status', 'created_at',)
    
    # Fields that can be searched using the search bar (search_fields)
    search_fields = ('filename', 'ocr_text',)

    # Fields that are read-only and cannot be edited via the form
    readonly_fields = ('created_at',)
    
    # Separate the fields into logical fieldsets for the edit form
    fieldsets = (
        ('File Details', {
            'fields': ('filename', 'file_size', 'created_at'),
        }),
        ('OCR Result', {
            'fields': ('ocr_text', 'status'),
        }),
    )

# 2. Register the model with its custom admin options
admin.site.register(OcrRecord, OcrRecordAdmin)