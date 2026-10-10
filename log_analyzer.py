import os
import sys

LOG_FILE = "security_audit.log"

print("==================================================")
print("   PUBLIC SECURITY DIGITAL FORENSICS TOOL ENGINE   ")
print("==================================================\n")

# 1. Verify that the log evidence file actually exists
if not os.path.exists(LOG_FILE):
    print(f"[x] ERROR: Could not locate evidence log file: '{LOG_FILE}'")
    print("Please run your central_brain.py server first to generate logs.")
    sys.exit(1)

# 2. Get user input for the target suspect query
target_suspect = input("[?] Enter the exact name of the suspect to analyze: ").strip()

match_count = 0
timestamps = []

# 3. Read and parse the file line-by-line
with open(LOG_FILE, "r") as file:
    for line in file:
        # Check if the line contains our target suspect query string
        if target_suspect.lower() in line.lower():
            match_count += 1
            # Extract the timestamp bracket out of the log line structure
            try:
                timestamp = line.split("]")[0].replace("[", "")
                timestamps.append(timestamp)
            except IndexError:
                pass

print("\n--------------------------------------------------")
print("               ANALYTICAL REPORT                  ")
print("--------------------------------------------------")

if match_count > 0:
    print(f"[!!!] TARGET IDENTIFIED IN HISTORICAL TRAIL")
    print(f"[+] Total Interceptions Logged:   {match_count} times")
    print(f"[+] First Spotted Timestamp:      {timestamps[0]}")
    print(f"[+] Latest Spotted Timestamp:     {timestamps[-1]}")
else:
    print(f"[i] Clear Status: No tracking logs found matching '{target_suspect}'.")

print("--------------------------------------------------")
