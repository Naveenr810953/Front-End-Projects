import asyncio
import websockets
import json
import random
from datetime import datetime

class NetworkAI:  
    def __init__(self):
        print("🧠 AI Model Initialized: Demo Mode")

    def analyze_packet(self, packet):
        payload = packet.get('payload', '')
        if "malware.exe" in payload:
            return "MALICIOUS", "Critical", "Malicious File Download Detected"
        if "UNION SELECT" in payload:
            return "MALICIOUS", "Critical", "SQL Injection Attack"
        return "BENIGN", "None", "Normal Traffic"

async def handler(websocket):
    print(f"✅ Client Connected: {websocket.remote_address}")
    ai = NetworkAI()
    packet_count = 0

    try:
        while True:
            packet_count += 1
            is_attack_time = (packet_count % 20 == 0)

            if is_attack_time:
                src_ip = f"192.168.1.{random.randint(100, 150)}"
                dest_ip = "45.33.22.11"
                dest_port = 80
                protocol = "HTTP"
                payload = "GET http://evil-hacker-site.com/downloads/malware.exe" 
                flag = "PSH"
                ttl = 64
            else:
                src_ip = f"192.168.1.{random.randint(2, 50)}"
                dest_ip = "10.0.0.5"
                dest_port = 443
                protocol = "HTTPS"
                payload = "Encrypted Traffic"
                flag = "ACK"
                ttl = 128

            packet_data = {
                "id": packet_count,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "src_ip": src_ip,
                "dest_ip": dest_ip,
                "src_port": random.randint(1024, 65535),
                "dest_port": dest_port,
                "protocol": protocol,
                "flags": flag,
                "length": random.randint(40, 1500),
                "ttl": ttl,
                "payload": payload
            }

            verdict, severity, description = ai.analyze_packet(packet_data)
            
            if verdict == "MALICIOUS":
                description = f"Malicious Link: {payload}"

            packet_data["ai_verdict"] = verdict
            packet_data["severity"] = severity
            packet_data["alert_msg"] = description

            await websocket.send(json.dumps(packet_data))
            await asyncio.sleep(1.0)

    except websockets.exceptions.ConnectionClosed:
        print("❌ Client Disconnected")

async def main():
    # UPDATED PORT HERE: 8766
    print("🚀 NIDS Server Started on ws://localhost:8766")
    async with websockets.serve(handler, "localhost", 8766):
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server Stopped")
