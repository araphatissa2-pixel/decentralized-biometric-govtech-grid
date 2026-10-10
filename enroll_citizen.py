import requests
import os
import sys
from deepface import DeepFace

REGISTER_URL = "http://localhost:8000/api/register_citizen"
API_HEADERS = {"x-api-key": "KALI_SECURE_TOKEN_2026"}

print("========================================================================")
print("     REPUBLIC OF LIBERIA - CENTRAL CITIZEN BIOMETRIC ENROLLMENT       ")
print("========================================================================\n")

photo_filename = "moses.jpg"
citizen_name = "President_Moses_Blah"
is_wanted = False  # Set to True if enrolling a wanted suspect target

if not os.path.exists(photo_filename):
    print(f"[x] CRITICAL SECURITY ERROR: Could not locate '{photo_filename}' in this folder.")
    print("[i] Please download the photo asset, name it 'moses.jpg', and save it here.")
    sys.exit(1)

print(f"[*] Parsing image boundary data grids for: {photo_filename}...")
print("[*] Generating 128-dimensional facial fingerprint vector using RetinaFace...")

try:
    # Extract authentic structural landmark coordinate strings from the real photograph
    objs = DeepFace.represent(img_path=photo_filename, model_name="Facenet", detector_backend="retinaface", enforce_detection=True)
    real_vector = objs[0]["embedding"]
    
    payload = {
        "name": citizen_name,
        "vector": real_vector,
        "is_wanted": is_wanted
    }
    
    # Securely stream the registration payload down the server line
    response = requests.post(REGISTER_URL, json=payload, headers=API_HEADERS, timeout=5)
    
    if response.status_code == 200:
        print("\n========================================================================")
        print(f"  [SUCCESS] NATIONAL BIOMETRIC REGISTRATION COMPLETED!")
        print(f"  [+] Profile Identity: {citizen_name}")
        print(f"  [+] Registry Status:  Officially locked into national database files.")
        print("========================================================================")
except Exception as e:
    print(f"\n[x] CRYPTO-AI PARSING ERROR: Face landmarks could not be traced. Error: {e}")
