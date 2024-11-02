from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import cv2
import numpy as np
from .src.ocr_utils import preprocess, ocr, classify_and_extract, validate_data
from .models import IDInfo

def home(request):
    return render(request, 'index.html')


def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        image_array = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        try:
            processed_img = preprocess(img)
            text = ocr(processed_img)
            print(text)
            data = classify_and_extract(text)

            print(data)
            
            if data and validate_data(data):
                IDInfo.objects.create(
                    id_type=data["id_type"],
                    id_number=data["id_number"],
                    name=data["name"],
                    dob=data["dob"],
                    encrypted_id_number=data["encrypted_id_number"],
                )
                return JsonResponse({"message": "Data Found", "data": data})
            else:
                return JsonResponse({"message": "Data validation failed or ID type not recognized."}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
