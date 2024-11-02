import pytesseract
import cv2
import numpy as np
import re
import hashlib

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess(img):
    '''Binarization of the image'''
    img_org = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    idim_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    r, threshed = cv2.threshold(idim_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    final_img = cv2.dilate(threshed, kernel, iterations=1)
    return final_img

def ocr(img):
    text = pytesseract.image_to_string(img, lang='eng')
    return text

def encrypt_id(id_number):
    sha512_hash = hashlib.sha512(id_number.encode('utf-8')).hexdigest()
    return sha512_hash

def validate_data(data):
    for key, value in data.items():
        if value is None or value.strip() == "":
            print(f"Validation Error: {key} cannot be empty.")
            return False
    return True

def classify_and_extract(text):
    data = {
        "id_type" : None,
        "id_number" : None,
        "name" : None,
        "dob" : None,
        "encrypted_id_number" : None
    }

    pan_pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'  # Matches PAN number pattern (5 letters, 4 digits, 1 letter)
    aadhaar_pattern = r'\d{4}\s\d{4}\s\d{4}'  # Aadhaar number pattern (12-digit number)

    if re.search(pan_pattern, text):
        name_pattern = r'Name\s*([A-Z\s]+)'   # Matches name field (capital letters)
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'  # Matches date format DD/MM/YYYY

        data["id_type"] = "PAN"
        try:
          data["id_number"] = re.search(pan_pattern, text).group(0).strip()
          data["name"] = re.search(name_pattern, text).group(1).strip()
          data["dob"] = re.search(dob_pattern, text).group(1).strip()
          data["encrypted_id_number"] = encrypt_id(data["id_number"])
        except:
          print("IMAGE NOT CLEAR OR NOT PROPERLY SCANNED !!!!!")
          return None

    elif re.search(aadhaar_pattern, text):
        name_pattern = r'([A-Z][a-z]+\s[A-Z][a-z]+)'
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'  # For date of birth
        
        data["id_type"] = "AADHAAR"
        try:
          data["id_number"] = re.search(aadhaar_pattern, text).group(0).strip()
          data["name"] = re.search(name_pattern, text).group(0).strip()
          data["dob"] = re.search(dob_pattern, text).group(1).strip()
          data["encrypted_id_number"] = encrypt_id(data["id_number"])
        except:
          print("IMAGE NOT CLEAR OR NOT PROPERLY SCANNED !!!!!")
          return None
    
    else:
        print("ID type not recognized")
        print("IMAGE NOT CLEAR OR NOT PROPERLY SCANNED !!!!!")
        return None

    return data

# def create_db():
#     conn = sqlite3.connect('id_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS id_info (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             id_type TEXT,
#             name TEXT,
#             dob TEXT,
#             encrypted_id_number TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def add_to_db(data):
#     conn = sqlite3.connect('id_data.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO id_info (id_type, name, dob, encrypted_id_number)
#         VALUES (?, ?, ?, ?)
#     ''', (data['id_type'], data['name'], data['dob'], data['encrypted_id_number']))
#     conn.commit()
#     conn.close()

