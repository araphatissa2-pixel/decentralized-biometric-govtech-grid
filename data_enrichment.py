import json
import os
import sys
import requests

UNKNOWN_DB_FILE = "unknown_targets_discovered.json"
REGISTER_URL = "http://localhost:8000/api/register_citizen"
API_HEADERS = {"x-api-key": "KALI_SECURE_TOKEN_2026"}

os.system('clear')
print("========================================================================")
print("     REPUBLIC OF LIBERIA - BIOMETRIC REGISTRY ENRICHMENT PANEL         ")
print("========================================================================")

# 1. Verify if any unknown targets have been discovered yet
if not os.path.exists(UNKNOWN_DB_FILE):
    print("\n[i] Status Clear: No unknown face profiles currently queued for review.")
    sys.exit(0)

with open(UNKNOWN_DB_FILE, "r") as f:
    try:
        unknown_targets = json.load(f)
    except:
        unknown_targets = {}

if not unknown_targets:
    print("\n[i] Status Clear: No unknown face profiles currently queued for review.")
    sys.exit(0)

print(f"[+] Found {len(unknown_targets)} anonymous profiles awaiting data enrichment.\n")
print(f"{'TARGET ID':<25} | {'FIRST SPOTTED TIME':<20} | {'LOCATION':<20}")
print("------------------------------------------------------------------------")
for target_id, info in unknown_targets.items():
    print(f"{target_id:<25} | {info['first_spotted_time']:<20} | {info['first_spotted_location']:<20}")
print("========================================================================")

# 2. Select target ID to modify
selected_id = input("\n[?] Enter the TARGET ID to enrich and promote (or press Enter to exit): ").strip()

if not selected_id or selected_id not in unknown_targets:
    print("[x] Error: Invalid Target ID selection parameters.")
    sys.exit(1)

target_data = unknown_targets[selected_id]

print(f"\n[*] Processing Profile: {selected_id}")
print(f"[*] First intercepted at: {target_data['first_spotted_location']}")

# 3. Gather citizen metadata input from the operator
citizen_name = input("[?] Enter the citizen's REAL FULL NAME for identification: ").strip()
status_choice = input("[?] Is this target currently WANTED BY THE LAW? (yes/no): ").strip().lower()
is_wanted = True if status_choice == "yes" else False

if not citizen_name:
    print("[x] Error: Citizen name parameters cannot be left blank.")
    sys.exit(1)

# 4. Transmit the profile to the central database server registry mapping
payload = {
    "name": citizen_name,
    "vector": target_data["vector"],
    "is_wanted": is_wanted
}

try:
    response = requests.post(REGISTER_URL, json=payload, headers=API_HEADERS, timeout=5)
    if response.status_code == 200:
        print(f"\n[SUCCESS] Profile promoted! '{citizen_name}' added to National Registry database.")
        
        # Remove the target from the temporary unknown database file to clear the queue
        del unknown_targets[selected_id]
        with open(UNKNOWN_DB_FILE, "w") as f:
            json.dump(unknown_targets, f, indent=4)
        print("[*] Temporary tracking target file safely purged from discovery queue.")
    else:
        print(f"[x] Ingestion Network Error: Server returned status code {response.status_code}")
except Exception as e:
    print(f"[x] Network Transmission Dropout: Server appears offline. Error: {e}")

print("========================================================================")
