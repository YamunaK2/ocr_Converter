# ocr_app/models.py (CORRECTED)

from django.db import models

class OcrRecord(models.Model):
    # Status choices for clarity and data validation
    STATUS_CHOICES = [
        ('Pending', 'Pending Processing'),
        ('Processed', 'Successfully Processed'),
        ('Error', 'Processing Error'),
    ]

    # File details
    filename = models.CharField(
        max_length=255, 
        null=False, 
        blank=False,
        help_text="Original name of the uploaded file."
    )
    
    # 🌟 CRITICAL CHANGE: The field that was missing and causing the error!
    image = models.ImageField(
        upload_to='ocr_images/',  # Files will be stored in media/ocr_images/
        help_text="The path to the uploaded image file."
    )

    file_size = models.IntegerField(
        help_text="Size of the file in bytes."
    )
    
    # OCR result
    ocr_text = models.TextField(
        help_text="The extracted text result from the OCR process."
    )
    
    # Status and timestamps
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Processing',  # Changed default to 'Processing' to better reflect Tesseract flow
        help_text="Processing status."
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Timestamp of when the record was created."
    )

    class Meta:
        # Define default ordering (newest records first)
        ordering = ['-created_at'] 
        verbose_name = "OCR Record"

    def __str__(self):
        # Include ID for uniqueness in logs/admin
        return f"Record {self.id} - {self.filename}"