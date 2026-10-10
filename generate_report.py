import json
import os
import sys

LOG_FILE = "security_audit.json"

# Clear the screen for a clean report dashboard interface
os.system('clear')

print("========================================================================")
print("             PUBLIC SECURITY COMMAND CENTER - FORENSIC REPORT            ")
print("========================================================================")

if not os.path.exists(LOG_FILE):
    print(f"\n[x] CRITICAL FORENSIC ERROR: Log archive file '{LOG_FILE}' not found.")
    print("[i] Please ensure your central_brain.py server is running and catching logs.")
    sys.exit(1)

print(f"| TARGET LOG DATABASE: {LOG_FILE}                                  |")
print("------------------------------------------------------------------------")
# Formatted Table Header Row
print(f"{'TIMESTAMP':<20} | {'CAMERA ID':<20} | {'LATENCY':<10} | {'IDENTIFICATION':<15}")
print("------------------------------------------------------------------------")

total_records = 0
sangel_count = 0
araphat_count = 0
unknown_count = 0

# Open and parse the production JSON log file line-by-line
with open(LOG_FILE, "r") as file:
    for line in file:
        if line.strip():
            try:
                # Load the raw string line as a dynamic JSON object dictionary
                log_data = json.loads(line)
                
                timestamp = log_data.get("timestamp", "N/A")
                camera = log_data.get("camera_node", "N/A")
                latency = f"{log_data.get('edge_latency_ms', 0.0)}ms"
                identity = log_data.get("identity_tag", "Unknown")
                
                # Print the aligned data row
                print(f"{timestamp:<20} | {camera:<20} | {latency:<10} | {identity:<15}")
                
                # Increment metrics
                total_records += 1
                if "sangel" in identity.lower():
                    sangel_count += 1
                elif "araphat" in identity.lower():
                    araphat_count += 1
                else:
                    unknown_count += 1
                    
            except json.JSONDecodeError:
                pass # Skip broken rows

print("========================================================================")
print("                      INTELLIGENCE METRICS SUMMARY                      ")
print("========================================================================")
print(f"  [+] Total Intercept Events Logged: {total_records}")
print(f"  [+] Suspect Sangel Capture Count:  {sangel_count}")
print(f"  [+] Suspect Araphat Capture Count: {araphat_count}")
print(f"  [+] Unknown Citizen Flags Raised:  {unknown_count}")
print("========================================================================")
