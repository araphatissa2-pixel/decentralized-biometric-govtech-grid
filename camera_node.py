import requests
import time
import os
import sys
from deepface import DeepFace

SERVER_URL = "http://localhost:8000/api/track"
CAMERA_ID = "STREET_CAM_KALI_405"
API_HEADERS = {"x-api-key": "KALI_SECURE_TOKEN_2026"}

print("====================================================================")
print("[*] REPUBLIC OF LIBERIA - ACTIVATING LIVE STRATEGIC PATROL MATRIX   ")
print("====================================================================\n")

real_target_photo = "moses.jpg"
if not os.path.exists(real_target_photo):
    print(f"[x] Critical Deployment Error: Real asset file '{real_target_photo}' missing.")
    print("[i] Please ensure your real photo file is saved in this directory.")
    sys.exit(1)

print(f"[+] Compiling biometric telemetry arrays for deployment...")
try:
    objs = DeepFace.represent(img_path=real_target_photo, model_name="Facenet", detector_backend="retinaface", enforce_detection=True)
    moses_vector = objs[0]["embedding"]
except Exception as e:
    print(f"[x] Diagnostic failure parsing '{real_target_photo}': {e}")
    sys.exit(1)

mock_unknown_vector = [0.85, -0.12, 0.99] + [0.1] * 125

print("\n[SUCCESS] Checkpoint nodes armed and broadcasting. Commencing surveillance loops...\n")

try:
    while True:
        print("\n[SENSING CHECKPOINT] Scanning Broad Street Traffic Hub Area...")
        start_time = time.time()
        time.sleep(0.045)
        latency = round((time.time() - start_time) * 1000, 2)
        
        try:
            requests.post(SERVER_URL, json={
                "camera_id": "MONROVIA_CHECKPOINT_01", 
                "location_marker": "Monrovia Broad St", 
                "face_vector": moses_vector,
                "processing_time_ms": latency
            }, headers=API_HEADERS, timeout=5)
        except Exception as e:
            print("    [x] Network transmission dropout.")
        time.sleep(4)
        
        print("\n[SENSING CHECKPOINT] Analyzing Inbound Passenger Lines at RIA Airport Entry...")
        start_time = time.time()
        time.sleep(0.048)
        latency = round((time.time() - start_time) * 1000, 2)
        
        try:
            requests.post(SERVER_URL, json={
                "camera_id": "RIA_AIRPORT_CAMERA", 
                "location_marker": "RIA Airport Entrance", 
                "face_vector": mock_unknown_vector,
                "processing_time_ms": latency
            }, headers=API_HEADERS, timeout=5)
        except Exception as e:
            print("    [x] Network transmission dropout.")
        time.sleep(4)

except KeyboardInterrupt:
    print("\n[-] Sensor sweeps halted.")
