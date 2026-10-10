import socket
import sys
from datetime import datetime

print("==================================================")
print("     DYNAMIC NETWORK BANNER-GRABBING SCANNER      ")
print("==================================================\n")

target_host = "127.0.0.1"

try:
    start_port = int(input("[?] Enter the STARTING port number (e.g., 7990): "))
    end_port = int(input("[?] Enter the ENDING port number (e.g., 8010): "))
except ValueError:
    print("[x] Error: Boundaries must be valid whole numbers.")
    sys.exit(1)

print(f"\n[*] Commencing banner-grab sweep on: {target_host}...")
print(f"[*] Clock execution index: {datetime.now().strftime('%H:%M:%S')}\n")

try:
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Balanced timeout for quick network responses
        
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f"  🚨 [ALERT] Open Port Found: {port}")
            
            try:
                # OFFENSIVE INFRASTRUCTURE UPGRADE: Send a basic request payload 
                # This forces web servers (like FastAPI) to speak back and reveal their identity banners
                s.send(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
                
                # Capture the first 512 bytes of data the port shoots back
                banner = s.recv(512).decode().strip()
                
                # Extract just the first line of the server banner to keep the display clean
                server_banner_line = "No explicit banner returned"
                for line in banner.split("\n"):
                    if "server" in line.lower():
                        server_banner_line = line.strip()
                        break
                
                print(f"      [=>] INTERCEPTED BANNER: {server_banner_line if banner else 'Service quiet.'}")
            except Exception as e:
                print("      [=>] INTERCEPTED BANNER: Connection established, but service remained silent.")
                
        s.close()

except KeyboardInterrupt:
    print("\n[-] Sweep halted by operator.")
    sys.exit(0)

print("\n==================================================")
print("               SCAN SWEEP COMPLETE                ")
print("==================================================")
