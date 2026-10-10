import socket
import struct
import sys

print("==================================================")
print("     ADVANCED TCP/UDP STRING DECODING SNIFFER     ")
print("==================================================\n")

print("[*] Initializing raw network interface hook...")

try:
    # Bind directly to all incoming link-layer frames via raw sockets
    sniffer_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    print("[+] Interface Armed: Decoding string payloads on the fly...\n")
except PermissionError:
    print("[x] CRITICAL ERROR: Raw sockets require root system access privileges.")
    print("[i] Please execute this tool using: 'sudo python packet_sniffer.py'")
    sys.exit(1)

packet_count = 0

try:
    while True:
        raw_data, addr = sniffer_socket.recvfrom(65535)
        packet_count += 1
        
        # 1. PARSE LINK-LAYER INTERFACE FRAME (First 14 Bytes)
        eth_header = raw_data[:14]
        eth_data = struct.unpack('!6s6sH', eth_header)
        
        dest_mac = ':'.join('%02x' % b for b in eth_data[0])
        src_mac = ':'.join('%02x' % b for b in eth_data[1])
        protocol_type = eth_data[2]
        
        # 2. ISOLATE IP NETWORK LAYER (EtherType 0x0800)
        if protocol_type == 0x0800:
            ip_header_raw = raw_data[14:34]
            ip_data = struct.unpack('!BBHHHBBH4s4s', ip_header_raw)
            
            src_ip = socket.inet_ntoa(ip_data[8])
            dest_ip = socket.inet_ntoa(ip_data[9])
            transport_proto = ip_data[6] # Identify inner protocol (6 = TCP, 17 = UDP)
            
            # Extract header length to find where the inner payload data begins
            ihl = (ip_data[0] & 0xF) * 4
            ip_payload_start = 14 + ihl
            
            # 3. TRANS-PORT DATA LAYER PARSING (TCP Protocol Segment Processing)
            if transport_proto == 6:
                tcp_header_raw = raw_data[ip_payload_start : ip_payload_start + 20]
                if len(tcp_header_raw) >= 20:
                    tcp_data = struct.unpack('!HHLLBBHHH', tcp_header_raw)
                    src_port = tcp_data[0]
                    dest_port = tcp_data[1]
                    
                    # Compute total size of the TCP options/header block
                    tcp_offset = (tcp_data[4] >> 4) * 4
                    data_offset = ip_payload_start + tcp_offset
                    
                    # Capture the raw residual binary string data inside the packet
                    payload_raw = raw_data[data_offset:]
                    
                    if payload_raw:
                        print(f" [#{packet_count:04}] 🚨 [LIVE INTERCEPT] TCP Payload Detected:")
                        print(f"      ├─ Route Pathway:   {src_ip}:{src_port} ➔ {dest_ip}:{dest_port}")
                        
                        try:
                            # Attempt to clean and print out human-readable ASCII text characters
                            ascii_payload = payload_raw.decode('utf-8', errors='ignore').strip()
                            # Clean out generic system alignment newlines to keep output compact
                            clean_payload = " ".join(ascii_payload.split())
                            
                            if clean_payload:
                                print(f"      └─ CAPTURED DATA:  {clean_payload[:180]}")
                                print("-" * 65)
                        except:
                            pass

except KeyboardInterrupt:
    print("\n[-] Sniffer capture process halted by operator request.")
    print(f"[+] Total network data frames audited: {packet_count}")
    sys.exit(0)
