from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import OcrRecord 

# Tesseract Imports and Image Processing
from PIL import Image
import pytesseract
import os # 🌟 os is imported for file deletion

# ⚠️ IMPORTANT: Set the path to the Tesseract executable for Windows
# The path must point to the tesseract.exe file.
try:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
except Exception as e:
    # This block is for warning only; the actual error is caught later in process_image
    print(f"WARNING: Could not set Tesseract command path. Tesseract may not be available. Error: {e}")


# =====================================================================
# Helper Function for Image Preprocessing
# =====================================================================

def binarize_image(image):
    """
    Converts a grayscale PIL Image to a strictly black/white (1-bit) image 
    using a fixed threshold of 128 to maximize contrast for Tesseract.
    """
    # '1' mode is 1-bit pixels, black and white, stored as 8-bit pixels
    return image.point(lambda x: 0 if x < 128 else 255, '1')


# =====================================================================
# API Endpoints
# =====================================================================

# 1. Status Check (handles GET /)
@require_http_methods(["GET"])
def status_check(request):
    """
    Returns a simple JSON response to verify the server is running.
    """
    return JsonResponse({
        "status": "OK",
        "message": "OCR API is connected to MySQL and running successfully.",
        "endpoints_available": [
            "/process_image/",
            "/records/",
            "/clear_records/"
        ]
    })

# 2. Process Image (handles POST /process_image/)
@csrf_exempt
@require_http_methods(["POST"])
def process_image(request):
    """
    Handles image upload, performs Tesseract OCR with preprocessing, and saves the result.
    """
    if not request.FILES or 'image' not in request.FILES:
        return JsonResponse({"success": False, "message": "No image file provided in the 'image' key."}, status=400)

    # Define new_record in function scope to satisfy static analyzers (Pylance)
    new_record = None 
    
    try:
        uploaded_file = request.FILES.get('image')
        
        # 1. Create the record and save the file to the 'media' directory
        new_record = OcrRecord.objects.create(
            filename=uploaded_file.name,
            file_size=uploaded_file.size,
            image=uploaded_file, # Saves the file using the ImageField
            ocr_text="Processing...", 
            status="Processing"
        )
        
        # 2. Perform OCR using the saved file's path and preprocessing
        image_path = new_record.image.path 
        
        # Open the image using Pillow
        with Image.open(image_path) as img:
            
            # Preprocessing Step A: Convert to Grayscale
            img_gray = img.convert('L') 
            
            # Preprocessing Step B: Apply Binarization (Thresholding)
            img_processed = binarize_image(img_gray)
            
            # Run Tesseract on the preprocessed image
            extracted_text = pytesseract.image_to_string(img_processed)
        
        # 3. Process result and determine final status
        if extracted_text.strip():
            final_text = extracted_text.strip()
            final_status = "Processed"
        else:
            final_text = "No recognizable text found."
            final_status = "Error"

        # 4. Update the record with the final OCR result
        new_record.ocr_text = final_text
        new_record.status = final_status
        new_record.save()

        return JsonResponse({
            "success": True, 
            "message": "Image processed successfully with Tesseract OCR.",
            "record_id": new_record.id,
            "result": final_text,
            "filename": new_record.filename
        })
        
    except pytesseract.TesseractNotFoundError:
        # If the record was created but Tesseract fails, update status to Error
        if new_record:
            new_record.status = "Error"
            new_record.ocr_text = "Tesseract executable not found."
            new_record.save()
            
        return JsonResponse({
            "success": False, 
            "message": "Tesseract executable not found. Check the path setting in views.py or installation.",
            "expected_path": pytesseract.pytesseract.tesseract_cmd 
        }, status=500)
        
    except Exception as e:
        # Catch other errors (e.g., file corruption, DB error)
        # If the record was created, update its status
        if new_record:
            new_record.status = "Error"
            new_record.ocr_text = f"Internal processing failed: {e}"
            new_record.save()
            
        return JsonResponse({"success": False, "message": f"Processing error: {e}"}, status=500)


# 3. Get Records (handles GET /records/)
@require_http_methods(["GET"])
def get_records(request):
    """
    Returns the list of all historical OCR records from the database.
    """
    try:
        # Fetch all records, ordered by creation date descending (newest first)
        records = OcrRecord.objects.all().values(
            'id', 'filename', 'file_size', 'ocr_text', 'status', 'created_at'
        )
        
        record_list = list(records)
        
        return JsonResponse({
            "success": True,
            "count": len(record_list),
            "records": record_list
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error fetching records: {e}"}, status=500)


# 4. Clear Records (handles POST /clear_records/)
@csrf_exempt
@require_http_methods(["POST"])
def clear_records(request):
    """
    Clears all stored historical OCR records from the database AND deletes the associated media files.
    """
    try:
        # 🌟 LOGIC CHANGE: Delete files from disk first
        records_to_delete = OcrRecord.objects.all()
        file_count = 0
        
        for record in records_to_delete:
            # Check if an image file exists and delete it
            # We use try/except just in case the file was manually deleted outside Django
            try:
                if record.image and os.path.exists(record.image.path):
                    os.remove(record.image.path)
                    file_count += 1
            except Exception as e:
                # Log file deletion errors but continue to delete the DB record
                print(f"Error deleting file for record ID {record.id}: {e}")
                
        
        # Then, delete the database records
        db_count, _ = records_to_delete.delete() # Deletes all records previously fetched
        
        return JsonResponse({
            "success": True,
            "message": f"Successfully cleared {db_count} database records and {file_count} associated image files.",
            "count_deleted": db_count,
            "files_deleted": file_count
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error clearing records: {e}"}, status=500)