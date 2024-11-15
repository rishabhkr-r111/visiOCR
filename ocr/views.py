from django.shortcuts import render, HttpResponse, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import cv2
import numpy as np
from .src.ocr_utils import preprocess, ocr, classify_and_extract, validate_data, convert_to_ist
from .models import IDInfo
import hashlib
import qrcode
from pyzbar.pyzbar import decode
from io import BytesIO
import base64

def home(request):
    return render(request, 'index.html')


def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        mobile_number = request.POST.get('mobile_number', None)
        valid_till = request.POST.get('valid_till', None)


        image_array = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        try:
            processed_img = preprocess(img)
            text = ocr(processed_img)
            print(text)
            data = classify_and_extract(text)
            data["mobile_number"] = mobile_number
            data["valid_till"] = valid_till
            print(data)
            print(timezone.now())
            print(datetime.now())
            
            if data and validate_data(data):
                unique_id_str = f"{data['encrypted_id_number']}{data['mobile_number']}{data['name']}"
                unique_id = hashlib.sha256(unique_id_str.encode()).hexdigest()

                if IDInfo.objects.filter(unique_id=unique_id).exists():
                    print("ID info already exists try after its pass expires.")
                    id_info = IDInfo.objects.get(unique_id=unique_id)
                    print(id_info.valid_till)
                    print(timezone.now())
                    if id_info.valid_till > timezone.now():
                        return HttpResponse({"<h2 style='text-align: center; color:red;'>PASS ALREADY EXISTS</h2> <h3 style='text-align: center;'>Cannot Create Duplicate Pass.</h3>"})
                    else:
                        id_info.delete()
                


                data["unique_id"] = unique_id

                 # Generate QR code
                qr = qrcode.make(unique_id)
                buffered = BytesIO()
                qr.save(buffered, format="PNG")
                qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                id_info = IDInfo.objects.create(
                    id_type=data["id_type"],
                    name=data["name"],
                    dob=data["dob"],
                    mobile_number=data["mobile_number"],
                    valid_till=data["valid_till"],
                    encrypted_id_number=data["encrypted_id_number"],
                    unique_id=unique_id
                )
                return render(request, 'visiting_card.html', {'id_info': data, 'qr_code': qr_base64, 'ist_time': convert_to_ist(data["valid_till"])})
            else:
                return JsonResponse({"message": "Data validation failed or ID type not recognized."}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def verify(request):
    return render(request, 'verify.html')



def verify_id(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        image_array = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        try:
            decoded_objects = decode(img)

            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')

                
                id_info = IDInfo.objects.filter(unique_id=qr_data).first()
                
                if id_info:
                    if id_info.valid_till > timezone.now():
                        id_info_dict = model_to_dict(id_info)
                        return render(request, 'verify_card.html', {'id_info': id_info_dict, 'ist_time': convert_to_ist(id_info.valid_till)})
                    else:
                        return render(request, 'invalid_card.html', {"message": "ID has expired."})
                else:
                    return render(request, 'invalid_card.html', {"message": "ID not found."})
            else:
                return render(request, 'invalid_card.html', {"message": "No QR code found in the image."})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



# def visiting_card(request, id):
#     try:
#         id_info = IDInfo.objects.get(id=id)
#         return render(request, 'visiting_card.html', {'id_info': id_info})
#     except IDInfo.DoesNotExist:
#         return JsonResponse({"error": "ID info not found."}, status=404)
