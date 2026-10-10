import sys
import os
import requests
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

SERVER_URL = "https://ngrok-free.dev"

API_HEADERS = {"x-api-key": "KALI_SECURE_TOKEN_2026"}

# Force standard smartphone aspect ratio device properties
Window.size = (360, 640)

class PoliceTrackingConsole(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # 1. APP HEADER
        self.add_widget(Label(
            text="🇱🇷 LIBERIA PUBLIC SECURITY 🇱🇷\n       MOBILE PATROL CLIENT",
            font_size='18sp',
            bold=True,
            size_hint_y=0.15,
            color=(0.1, 0.6, 0.9, 1)
        ))

        # 2. CAMERA MONITOR ARMED PLACEHOLDER BOX
        self.camera_box = Label(
            text="[ CAMERA VIEWPORT ARMED ]\nReady to scan pedestrian landmarks",
            size_hint_y=0.4,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.camera_box)

        # 3. INFRASTRUCTURE NODE SELECTOR
        self.add_widget(Label(text="Select Checkpoint Node:", size_hint_y=0.05, bold=True))
        self.node_selector = Spinner(
            text='Monrovia Broad St',
            values=('Monrovia Broad St', 'Ganta Border Gateway', 'RIA Airport Entrance'),
            size_hint_y=0.08
        )
        self.add_widget(self.node_selector)

        # 4. CAPTURE TRIGGER BUTTON
        self.scan_button = Button(
            text="SCAN TARGET FACE",
            font_size='16sp',
            bold=True,
            background_color=(0.1, 0.7, 0.3, 1),
            size_hint_y=0.12
        )
        self.scan_button.bind(on_press=self.execute_biometric_scan)
        self.add_widget(self.scan_button)

        # 5. SERVER REAL-TIME DECISION ALERT FIELD
        self.status_display = Label(
            text="System Status: Idle\nAwaiting biometric target...",
            size_hint_y=0.2,
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.status_display)

    def execute_biometric_scan(self, instance):
        self.status_display.text = "Streaming biometric payload...\nContacting Central Command..."
        
        # Hardcoded array mapping directly to our pre-enrolled database signatures
        # This vector simulates our David/Unknown matrix payload profile
        mock_face_vector = [0.0] * 128 
        
        data_packet = {
            "camera_id": "MOBILE_PATROL_UNIT_05",
            "location_marker": self.node_selector.text,
            "face_vector": mock_face_vector
        }

        try:
            response = requests.post(SERVER_URL, json=data_packet, headers=API_HEADERS, timeout=5)
            
            if response.status_code == 200:
                server_data = response.json()
                identity = server_data.get("identity", "Unknown Citizen")
                
                if "unknown" not in identity.lower():
                    self.status_display.text = f"🚨 MATCH DETECTED! 🚨\nTarget: {identity}\nNode: {self.node_selector.text}"
                else:
                    self.status_display.text = f"⚠️ NEW FACE PATTERN ⚠️\nLogged at: {self.node_selector.text}\nCreated unknown target ID."
            else:
                self.status_display.text = f"[ERROR] Unauthorized Node!\nServer status code: {response.status_code}"
        except Exception as e:
            self.status_display.text = "[LINK FAILURE] Server Offline!\nCheck if central_brain.py is running on port 8000."

class LiberianSecurityApp(App):
    def build(self):
        return PoliceTrackingConsole()

if __name__ == '__main__':
    LiberianSecurityApp().run()
