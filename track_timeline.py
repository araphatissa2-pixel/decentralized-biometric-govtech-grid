import os
import sys

LOG_FILE = "security_audit.log"

os.system('clear')

print("========================================================================")
print("       REPUBLIC OF LIBERIA - NATIONAL BIOMETRIC INTELLIGENCE ENGINE     ")
print("                     FUGITIVE MOVEMENT TIMELINE TRACKER                 ")
print("========================================================================\n")

if not os.path.exists(LOG_FILE):
    print(f"[x] ERROR: Could not locate tracking log file: '{LOG_FILE}'")
    print("[i] Please tap 'SCAN TARGET FACE' on your app a few times first to make data.")
    sys.exit(1)

target_query = input("[?] Enter the suspect name to generate timeline (e.g., david): ").strip()

if not target_query:
    print("[x] Error: Search target parameters cannot be blank.")
    sys.exit(1)

timeline_records = []

# Process our plain text log structure lines natively without JSON formatting constraints
with open(LOG_FILE, "r") as file:
    for line in file:
        if line.strip() and target_query.lower() in line.lower():
            timeline_records.append(line.strip())

print("\n------------------------------------------------------------------------")
print(f"            CHRONOLOGICAL TRACKING ANALYSIS: {target_query.upper()}     ")
print("------------------------------------------------------------------------")

if timeline_records:
    print(f"[!!!] ALERT: {len(timeline_records)} WATCHLIST INTERCEPTIONS RETRIEVED.\n")
    for idx, record in enumerate(timeline_records, 1):
        print(f"  [{idx}] {record}")
    print("-" * 72)
    print(f"[+] Operational Summary: Target footprint verified inside system logs.")
else:
    print(f"[i] Search Status Clear: No historical tracking footprints found for '{target_query}'.")

print("========================================================================")
# Keeps the terminal session locked open so the report results never disappear
input("\n[i] Press ENTER to close the forensic report...")
