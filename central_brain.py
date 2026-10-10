from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import math
import os

app = FastAPI(title="Smart Liberian National Biometric Registry Engine")

class ScanPayload(BaseModel):
    camera_id: str
    location_marker: str
    face_vector: List[float]

SECRET_API_KEY = "KALI_SECURE_TOKEN_2026"
LOG_FILE = "security_audit.log"

CITIZEN_DB_FILE = "national_citizen_registry.json"
WANTED_LIST_FILE = "national_wanted_list.json"
UNKNOWN_LOG_FILE = "unknown_targets_discovered.json"

def load_db(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_db(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

citizens = load_db(CITIZEN_DB_FILE)
wanted_list = load_db(WANTED_LIST_FILE)
unknown_discovered = load_db(UNKNOWN_LOG_FILE)

@app.post("/api/register_citizen")
def register_citizen(payload: dict, x_api_key: Optional[str] = Header(None)):
    if x_api_key != SECRET_API_KEY: raise HTTPException(status_code=401)
    name = payload.get("name")
    vector = payload.get("vector")
    is_wanted = payload.get("is_wanted", False)
    
    citizens[name] = vector
    wanted_list[name] = is_wanted
    save_db(citizens, CITIZEN_DB_FILE)
    save_db(wanted_list, WANTED_LIST_FILE)
    print(f"[REGISTRY DATA] Enrolled Citizen Profile: {name} (Wanted Status: {is_wanted})")
    return {"status": "SUCCESS"}

@app.post("/api/track")
def process_surveillance_feed(payload: ScanPayload, x_api_key: Optional[str] = Header(None)):
    if x_api_key != SECRET_API_KEY: raise HTTPException(status_code=401)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    incoming_vector = payload.face_vector
    
    best_match = None
    min_distance = 999.0
    
    for citizen_name, stored_vector in citizens.items():
        if len(incoming_vector) == len(stored_vector):
            squared_diffs = sum((x - y) ** 2 for x, y in zip(incoming_vector, stored_vector))
            distance = math.sqrt(squared_diffs)
            if distance < 0.60 and distance < min_distance:
                min_distance = distance
                best_match = citizen_name

    os.system('clear')
    print("=====================================================================")
    print("      REPUBLIC OF LIBERIA - SMART BIOMETRIC SURVEILLANCE DATA       ")
    print("=====================================================================")
    print(f"| SENSOR LOCATION: {payload.location_marker:<20} | TIME: {current_time} |")
    print("---------------------------------------------------------------------")

    identified_name = "Unknown Citizen"
    status_flag = "CLEAR / CITIZEN"

    if best_match:
        identified_name = best_match
        status_flag = "CRIMINAL WANTED" if wanted_list.get(best_match, False) else "CLEAR / CITIZEN"
        print(f"  [+] PROFILE MATCHED:    {best_match}")
        print(f"  [+] DISPOSITION METRIC: {status_flag}")
        print(f"  [+] BIOMETRIC GEOMETRY: Confirmed match confidence: {round((1-min_distance)*100,2)}% ")
        if status_flag == "CRIMINAL WANTED":
            print("\n  🚨  [CRITICAL ALARM] SUSPECT DEVIATION INTERCEPTED! DISPATCH UNIT! 🚨")
    else:
        existing_unknown_match = None
        min_unknown_distance = 999.0
        
        for unk_id, unk_info in unknown_discovered.items():
            stored_unk_vector = unk_info["vector"]
            squared_diffs = sum((x - y) ** 2 for x, y in zip(incoming_vector, stored_unk_vector))
            distance = math.sqrt(squared_diffs)
            if distance < 0.60 and distance < min_unknown_distance:
                min_unknown_distance = distance
                existing_unknown_match = unk_id
                
        if existing_unknown_match:
            print(f"  ⚠️  [DETECTION FEEDS] REPEAT ANONYMOUS VISITOR SPOTTED! ⚠️")
            print(f"  [i] Tracking Target ID: {existing_unknown_match}")
            unknown_discovered[existing_unknown_match]["last_seen_time"] = current_time
            unknown_discovered[existing_unknown_match]["last_seen_location"] = payload.location_marker
        else:
            new_id = f"UNKNOWN_TARGET_ID_{len(unknown_discovered) + 1001}"
            print(f"  ⚠️  [DETECTION FEEDS] NEW ANONYMOUS FACE PATTERN SPOTTED! ⚠️")
            print(f"  [i] Created Target ID:  {new_id}")
            unknown_discovered[new_id] = {
                "first_spotted_time": current_time,
                "first_spotted_location": payload.location_marker,
                "last_seen_time": current_time,
                "last_seen_location": payload.location_marker,
                "vector": incoming_vector
            }
            
        save_db(unknown_discovered, UNKNOWN_LOG_FILE)
        
    # FORENSIC LOGGING COMPLIANCE: Unconditionally record every intercept entry to disk
    with open(LOG_FILE, "a") as log_file:
        log_line = f"[{current_time}] [{identified_name}] spotted at node {payload.camera_id} via {payload.location_marker} ({status_flag})\n"
        log_file.write(log_line)
        
    print("=====================================================================")
    return {"status": "PROCESSED", "identity": identified_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
