import os
import sys
import time
import threading
from datetime import datetime

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import cv2
import numpy as np
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

from config import (
    PROJECT_NAME,
    RGB_CAMERA_ID,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    ALERT_CLASSES
)

class Dashboard:
    def __init__(
        self,
        detector=None,
        thermal_classifier=None,
        fusion_engine=None,
        database=None,
        alert_manager=None,
        report_generator=None,
        evidence_manager=None,
        analytics_manager=None,
        camera=None
    ):
        self.detector = detector
        self.thermal_classifier = thermal_classifier
        self.fusion_engine = fusion_engine
        self.database = database
        self.alert_manager = alert_manager
        self.report_generator = report_generator
        self.evidence_manager = evidence_manager
        self.analytics_manager = analytics_manager
        self.camera = camera

        self.is_running = True
        self.voice_enabled = True
        self.last_voice_time = 0

        self.prev_time = time.time()
        self.fps = 30

        self.session_objects = {}
        self.unique_persons = set()
        self.unique_vehicles = set()
        self.tracked_positions = {}
        self.total_line_crossings = 0
        self.active_proximity_alerts = 0

        self.roi_points = []         
        self.is_roi_complete = False  
        self.roi_intrusion_count = 0  

        self.wa_instance_id = "710722691534"      
        self.wa_api_token = "786df8e435974da8ad78326fb15599f7b892cead5a2947bdb9"          
        self.wa_chat_id = "918830150755@c.us"              
        self.whatsapp_enabled = True
        self.last_whatsapp_time = 0
        self.whatsapp_cooldown = 8.0

        self.evidence_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "evidence"))
        self.snapshots_dir = os.path.join(self.evidence_dir, "snapshots")
        self.videos_dir = os.path.join(self.evidence_dir, "videos")
        
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)

        self.is_recording = False
        self.manual_recording = False
        self.video_writer = None
        self.recording_start_time = 0
        self.recording_duration = 10.0
        self.last_snapshot_time = 0
        self.snapshot_cooldown = 5.0                       

        if self.camera is None:
            self.camera = cv2.VideoCapture(RGB_CAMERA_ID)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        self.root = tk.Tk()
        self.root.title(f"{PROJECT_NAME} - M.Tech Research Edition")
        self.root.geometry("1366x768")
        self.root.configure(bg="#030712")

        self.setup_ui()

    def setup_ui(self):
        """M.Tech Grade Professional UI Layout Setup with Optimized Panel Fitting"""

        self.header_frame = tk.Frame(self.root, bg="#0B132B", height=45)
        self.header_frame.pack(side=tk.TOP, fill=tk.X, padx=8, pady=(6, 2))

        self.header_title = tk.Label(
            self.header_frame,
            text="⚡ AI-BASED MULTI-SCOPE OBJECT DETECTION & CLASSIFICATION SYSTEM",
            font=("Consolas", 13, "bold"),
            bg="#0B132B",
            fg="#38BDF8"
        )
        self.header_title.pack(side=tk.LEFT, padx=12)

        self.clock_label = tk.Label(
            self.header_frame,
            text="",
            font=("Consolas", 11, "bold"),
            bg="#0B132B",
            fg="#10B981"
        )
        self.clock_label.pack(side=tk.RIGHT, padx=12)
        self.update_clock()

        self.main_container = tk.Frame(self.root, bg="#030712")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # RIGHT SIDE ANALYTICS & CONTROL PANEL
        self.right_panel = tk.Frame(self.main_container, bg="#0F172A", width=380, highlightbackground="#1E293B", highlightthickness=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
        self.right_panel.pack_propagate(False)

        tk.Label(
            self.right_panel,
            text="LIVE TELEMETRY & ANALYTICS",
            font=("Consolas", 11, "bold"),
            bg="#0F172A",
            fg="#F8FAFC"
        ).pack(pady=(8, 4))

        self.metrics_frame = tk.Frame(self.right_panel, bg="#0F172A")
        self.metrics_frame.pack(fill=tk.X, padx=8, pady=2)

        c1 = tk.Frame(self.metrics_frame, bg="#1E293B", bd=1, relief=tk.SOLID)
        c1.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Label(c1, text="PERSONS", font=("Consolas", 8, "bold"), bg="#1E293B", fg="#94A3B8").pack(anchor="w", padx=5, pady=(2, 0))
        self.val_persons = tk.Label(c1, text="0", font=("Consolas", 14, "bold"), bg="#1E293B", fg="#38BDF8")
        self.val_persons.pack(anchor="w", padx=5, pady=(0, 2))

        c2 = tk.Frame(self.metrics_frame, bg="#1E293B", bd=1, relief=tk.SOLID)
        c2.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        tk.Label(c2, text="VEHICLES", font=("Consolas", 8, "bold"), bg="#1E293B", fg="#94A3B8").pack(anchor="w", padx=5, pady=(2, 0))
        self.val_vehicles = tk.Label(c2, text="0", font=("Consolas", 14, "bold"), bg="#1E293B", fg="#38BDF8")
        self.val_vehicles.pack(anchor="w", padx=5, pady=(0, 2))

        c3 = tk.Frame(self.metrics_frame, bg="#1E293B", bd=1, relief=tk.SOLID)
        c3.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        tk.Label(c3, text="TRIPWIRE HITS", font=("Consolas", 8, "bold"), bg="#1E293B", fg="#94A3B8").pack(anchor="w", padx=5, pady=(2, 0))
        self.val_trips = tk.Label(c3, text="0", font=("Consolas", 14, "bold"), bg="#1E293B", fg="#FACC15")
        self.val_trips.pack(anchor="w", padx=5, pady=(0, 2))

        c4 = tk.Frame(self.metrics_frame, bg="#1E293B", bd=1, relief=tk.SOLID)
        c4.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        tk.Label(c4, text="PROXIMITY ALERTS", font=("Consolas", 8, "bold"), bg="#1E293B", fg="#94A3B8").pack(anchor="w", padx=5, pady=(2, 0))
        self.val_alerts = tk.Label(c4, text="0", font=("Consolas", 14, "bold"), bg="#1E293B", fg="#EF4444")
        self.val_alerts.pack(anchor="w", padx=5, pady=(0, 2))

        self.metrics_frame.columnconfigure(0, weight=1)
        self.metrics_frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self.right_panel, bg="#0F172A")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(4, 8))

        self.voice_button = tk.Button(
            btn_frame,
            text="🔊 VOICE ALERT : ON",
            command=self.toggle_voice,
            bg="#0284C7",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        self.voice_button.pack(fill=tk.X, pady=2)

        self.whatsapp_button = tk.Button(
            btn_frame,
            text="💬 WHATSAPP NOTIFY : ON",
            command=self.toggle_whatsapp,
            bg="#16A34A",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        self.whatsapp_button.pack(fill=tk.X, pady=2)

        self.rec_button = tk.Button(
            btn_frame,
            text="📹 MANUAL REC : OFF",
            command=self.toggle_manual_recording,
            bg="#64748B",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        self.rec_button.pack(fill=tk.X, pady=2)

        csv_button = tk.Button(
            btn_frame,
            text="📁 EXPORT CSV LOGS",
            command=self.export_csv,
            bg="#059669",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        csv_button.pack(fill=tk.X, pady=2)

        excel_button = tk.Button(
            btn_frame,
            text="📊 EXPORT EXCEL REPORT",
            command=self.export_excel,
            bg="#15803D",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        excel_button.pack(fill=tk.X, pady=2)

        pdf_button = tk.Button(
            btn_frame,
            text="📄 GENERATE EXECUTIVE PDF REPORT",
            command=self.export_pdf,
            bg="#7C3AED",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        pdf_button.pack(fill=tk.X, pady=2)

        shutdown_button = tk.Button(
            btn_frame,
            text="🚨 EMERGENCY SHUTDOWN",
            command=self.shutdown,
            bg="#DC2626",
            fg="white",
            font=("Consolas", 8, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            pady=3
        )
        shutdown_button.pack(fill=tk.X, pady=2)

        tk.Label(
            self.right_panel,
            text="REAL-TIME TELEMETRY LOGS",
            font=("Consolas", 9, "bold"),
            bg="#0F172A",
            fg="#94A3B8"
        ).pack(pady=(6, 2))

        self.log_box = scrolledtext.ScrolledText(
            self.right_panel,
            wrap=tk.WORD,
            bg="#030712",
            fg="#22C55E",
            font=("Consolas", 8),
            relief=tk.FLAT,
            bd=1,
            height=8,
            highlightbackground="#1E293B",
            highlightthickness=1
        )
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=8, pady=2)

        self.left_panel = tk.Frame(self.main_container, bg="black", highlightbackground="#1E293B", highlightthickness=1)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.video_label = tk.Label(self.left_panel, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        self.video_label.bind("<Button-1>", self.handle_video_click)
        self.video_label.bind("<Button-3>", self.handle_video_click)

    def toggle_manual_recording(self):
        """Toggles manual video recording ON and OFF"""
        if not self.is_recording:
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"manual_rec_{time_str}.avi"
            filepath = os.path.join(self.videos_dir, filename)

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(filepath, fourcc, 15.0, (CAMERA_WIDTH, CAMERA_HEIGHT))
            
            self.is_recording = True
            self.manual_recording = True
            self.rec_button.config(text="🔴 MANUAL REC : ON", bg="#DC2626")
            self.append_log(f"EVIDENCE: 🔴 Manual Video Recording Started -> {filename}")
        else:
            self.is_recording = False
            self.manual_recording = False
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            self.rec_button.config(text="📹 MANUAL REC : OFF", bg="#64748B")
            self.append_log("EVIDENCE: ⏹️ Video Recording Stopped & Saved.")

    def save_local_snapshot(self, frame, track_id, label):
        """Saves high-res snapshot image locally to evidence/snapshots/"""
        curr_time = time.time()
        if curr_time - self.last_snapshot_time > self.snapshot_cooldown:
            self.last_snapshot_time = curr_time
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{time_str}_ID{track_id}_{label.upper()}.jpg"
            filepath = os.path.join(self.snapshots_dir, filename)
            
            cv2.imwrite(filepath, frame)
            self.append_log(f"EVIDENCE: Snapshot saved -> {filename}")

    def trigger_auto_recording(self, frame):
        """Starts 10-second automatic evidence video recording if not already recording"""
        if not self.is_recording:
            self.is_recording = True
            self.manual_recording = False
            self.recording_start_time = time.time()
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evidence_clip_{time_str}.avi"
            filepath = os.path.join(self.videos_dir, filename)

            h, w = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(filepath, fourcc, 15.0, (w, h))
            self.append_log(f"EVIDENCE: 🔴 Auto Video Recording Started -> {filename}")

    def process_video_recording(self, frame):
        """Writes frames to video writer and handles timeout for auto-recording"""
        if self.is_recording and self.video_writer is not None:
            rec_text = "🔴 REC - MANUAL RECORDING" if self.manual_recording else "🔴 REC - AUTO EVIDENCE RECORDING"
            cv2.putText(frame, rec_text, (15, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2, cv2.LINE_AA)
            
            self.video_writer.write(frame)

            if not self.manual_recording:
                if time.time() - self.recording_start_time >= self.recording_duration:
                    self.is_recording = False
                    self.video_writer.release()
                    self.video_writer = None
                    self.append_log("EVIDENCE: ⏹️ Auto Video Clip Recording Completed & Saved.")

    def _whatsapp_worker(self, image_frame, caption):
        try:
            if not self.wa_instance_id or "YOUR_INSTANCE" in self.wa_instance_id:
                return

            success, buffer = cv2.imencode('.jpg', image_frame)
            if not success:
                return

            url = f"https://api.green-api.com/waInstance{self.wa_instance_id}/sendFileByUpload/{self.wa_api_token}"
            payload = {'chatId': self.wa_chat_id, 'caption': caption}
            files = [('file', ('alert.jpg', buffer.tobytes(), 'image/jpeg'))]

            response = requests.post(url, data=payload, files=files, timeout=12)
            
            if response.status_code == 200:
                print("✅ [WHATSAPP SUCCESS] Photo Snapshot Alert Sent Successfully!")
            else:
                text_url = f"https://api.green-api.com/waInstance{self.wa_instance_id}/sendMessage/{self.wa_api_token}"
                text_payload = {"chatId": self.wa_chat_id, "message": caption}
                text_resp = requests.post(text_url, json=text_payload, timeout=8)
                if text_resp.status_code == 200:
                    print("✅ [WHATSAPP SUCCESS] Text Alert Sent Successfully!")

        except Exception as e:
            print(f"❌ [WHATSAPP EXCEPTION] Failed to send WhatsApp alert: {e}")

    def send_whatsapp_alert(self, frame, caption):
        current_time = time.time()
        if self.whatsapp_enabled and (current_time - self.last_whatsapp_time > self.whatsapp_cooldown):
            self.last_whatsapp_time = current_time
            self.append_log("WHATSAPP: Dispatching Instant Photo Snapshot Alert...")
            t = threading.Thread(target=self._whatsapp_worker, args=(frame.copy(), caption), daemon=True)
            t.start()

    def toggle_whatsapp(self):
        self.whatsapp_enabled = not self.whatsapp_enabled
        if self.whatsapp_enabled:
            self.whatsapp_button.config(text="💬 WHATSAPP NOTIFY : ON", bg="#16A34A")
            self.append_log("SYSTEM: WhatsApp alerts enabled.")
        else:
            self.whatsapp_button.config(text="💬 WHATSAPP NOTIFY : OFF", bg="#64748B")
            self.append_log("SYSTEM: WhatsApp alerts disabled.")

    def handle_video_click(self, event):
        if event.num == 3:  
            self.roi_points.clear()
            self.is_roi_complete = False
            self.append_log("SYSTEM: Restricted Danger Zone Cleared.")
            return

        if event.num == 1:  
            if len(self.roi_points) < 4:
                lbl_w = max(1, self.video_label.winfo_width())
                lbl_h = max(1, self.video_label.winfo_height())

                scale_x = CAMERA_WIDTH / lbl_w
                scale_y = CAMERA_HEIGHT / lbl_h

                frame_x = int(event.x * scale_x)
                frame_y = int(event.y * scale_y)

                self.roi_points.append((frame_x, frame_y))
                self.append_log(f"ROI Point {len(self.roi_points)}/4 Added at ({frame_x}, {frame_y})")

                if len(self.roi_points) == 4:
                    self.is_roi_complete = True
                    self.append_log("ALERT: RESTRICTED DANGER ZONE ACTIVATED (4/4 Points Set)!")

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def append_log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{timestamp}] {text}\n")
        self.log_box.see(tk.END)

    def draw_tactical_hud(self, frame, fps_val):
        h, w = frame.shape[:2]

        hud_text = f"[AI CORE: ONLINE] [FPS: {fps_val}] [MODEL: YOLOv8+CNN]"
        cv2.putText(frame, hud_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA)

        clen = 25
        cv2.line(frame, (10, 10), (10 + clen, 10), (0, 255, 255), 2)
        cv2.line(frame, (10, 10), (10, 10 + clen), (0, 255, 255), 2)
        cv2.line(frame, (w - 10, 10), (w - 10 - clen, 10), (0, 255, 255), 2)
        cv2.line(frame, (w - 10, 10), (w - 10, 10 + clen), (0, 255, 255), 2)
        cv2.line(frame, (10, h - 10), (10 + clen, h - 10), (0, 255, 255), 2)
        cv2.line(frame, (10, h - 10), (10, h - 10 - clen), (0, 255, 255), 2)
        cv2.line(frame, (w - 10, h - 10), (w - 10 - clen, h - 10), (0, 255, 255), 2)
        cv2.line(frame, (w - 10, h - 10), (w - 10, h - 10 - clen), (0, 255, 255), 2)

    def process_detection_pipeline(self, frame):
        annotated_frame = frame.copy()
        raw_detections = []

        curr_time = time.time()
        fps_val = int(1.0 / (curr_time - self.prev_time + 1e-5))
        self.prev_time = curr_time

        self.draw_tactical_hud(annotated_frame, fps_val)

        if self.detector is not None:
            try:
                if hasattr(self.detector, 'detect_and_track'):
                    raw_detections = self.detector.detect_and_track(frame)
                elif hasattr(self.detector, 'detect'):
                    raw_detections = self.detector.detect(frame)
            except Exception as e:
                print(f"[DETECTION ERROR] {e}")

        h, w = frame.shape[:2]
        tripwire_y = int(h * 0.58)

        cv2.line(annotated_frame, (0, tripwire_y), (w, tripwire_y), (255, 255, 0), 2)
        cv2.putText(annotated_frame, "AI TRIPWIRE LINE (ANALYTICS)", (12, tripwire_y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1, cv2.LINE_AA)

        if len(self.roi_points) > 0:
            for pt in self.roi_points:
                cv2.circle(annotated_frame, pt, 5, (0, 255, 255), -1)

        if len(self.roi_points) >= 2 and not self.is_roi_complete:
            pts = np.array(self.roi_points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [pts], isClosed=False, color=(0, 255, 255), thickness=2)

        if self.is_roi_complete:
            roi_poly = np.array(self.roi_points, np.int32).reshape((-1, 1, 2))
            overlay = annotated_frame.copy()
            cv2.fillPoly(overlay, [roi_poly], (0, 0, 255))
            cv2.addWeighted(overlay, 0.25, annotated_frame, 0.75, 0, annotated_frame)
            cv2.polylines(annotated_frame, [roi_poly], isClosed=True, color=(0, 0, 255), thickness=2)

            cv2.putText(annotated_frame, "[RESTRICTED DANGER ZONE]", 
                        (self.roi_points[0][0], max(25, self.roi_points[0][1] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

        current_active_alerts = 0
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for det in raw_detections:
            track_id = det.get('track_id', -1)
            label = det.get('label', 'object')
            conf = det.get('confidence', 0.0)
            bbox = det.get('bbox', [0, 0, 0, 0])
            dist = det.get('distance', 1.0)
            status = det.get('status', 'SAFE')

            x1, y1, x2, y2 = bbox
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            center_y = cy

            in_restricted_zone = False
            if self.is_roi_complete:
                roi_poly = np.array(self.roi_points, np.int32).reshape((-1, 1, 2))
                is_inside = cv2.pointPolygonTest(roi_poly, (cx, cy), False)
                if is_inside >= 0:
                    in_restricted_zone = True

            is_critical_close = (dist <= 1.5 and label.lower() == 'person')

            if in_restricted_zone or is_critical_close:
                status = "CRITICAL"
                if in_restricted_zone:
                    self.roi_intrusion_count += 1
                    alert_type = "RESTRICTED ZONE INTRUSION"
                    self.append_log(f"CRITICAL: {label.upper()} (#{track_id}) INTRUDED RESTRICTED ZONE!")
                else:
                    alert_type = "PROXIMITY WARNING (< 1.5m)"
                    self.append_log(f"ALERT: {label.upper()} (#{track_id}) AT {dist}m TRIGGERED ALARM!")

                caption = (
                    f"🚨 *SECURITY ALERT DETECTED!* 🚨\n\n"
                    f"⚠️ *Event:* {alert_type}\n"
                    f"📌 *Object:* {label.upper()}\n"
                    f"🆔 *Track ID:* #{track_id}\n"
                    f"📏 *Distance:* {dist}m\n"
                    f"⏰ *Time:* {now_str}\n"
                    f"📍 *System:* Multi-Scope AI Engine"
                )
                self.send_whatsapp_alert(annotated_frame, caption)
                self.save_local_snapshot(annotated_frame, track_id, label)
                self.trigger_auto_recording(annotated_frame)

            if label.lower() == 'person':
                self.unique_persons.add(track_id)
            elif label.lower() in ['car', 'bus', 'truck', 'motorbike', 'bicycle']:
                self.unique_vehicles.add(track_id)

            if status in ["CRITICAL", "WARNING"] or dist < 3.0 or in_restricted_zone:
                current_active_alerts += 1

            if track_id not in self.session_objects:
                self.session_objects[track_id] = {
                    "track_id": track_id,
                    "label": label,
                    "confidence": conf,
                    "max_confidence": conf,
                    "min_distance": dist,
                    "status": status,
                    "first_seen": now_str,
                    "last_seen": now_str,
                    "crossings": 0
                }
            else:
                s_obj = self.session_objects[track_id]
                s_obj["max_confidence"] = max(s_obj["max_confidence"], conf)
                s_obj["min_distance"] = min(s_obj["min_distance"], dist)
                s_obj["status"] = status
                s_obj["last_seen"] = now_str

            box_color = (0, 0, 255) if (status == "CRITICAL" or dist < 1.5 or in_restricted_zone) else (0, 255, 0)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), box_color, 2)

            caption_box = f"ID:{track_id} {label} {dist}m"
            if in_restricted_zone or is_critical_close:
                caption_box += " [ALARM!]"

            (tw, th), _ = cv2.getTextSize(caption_box, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated_frame, (x1, max(0, y1 - 22)), (x1 + tw + 6, max(20, y1)), box_color, -1)
            cv2.putText(annotated_frame, caption_box, (x1 + 3, max(15, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

            if track_id in self.tracked_positions:
                prev_y = self.tracked_positions[track_id]
                if prev_y < tripwire_y <= center_y:
                    self.total_line_crossings += 1
                    self.session_objects[track_id]["crossings"] += 1
                    self.append_log(f"TRIPWIRE: {label.upper()} (#{track_id}) crossed down [ENTRY]")
                elif prev_y > tripwire_y >= center_y:
                    self.total_line_crossings += 1
                    self.session_objects[track_id]["crossings"] += 1
                    self.append_log(f"TRIPWIRE: {label.upper()} (#{track_id}) crossed up [EXIT]")

            self.tracked_positions[track_id] = center_y

            current_time = time.time()
            if self.voice_enabled and self.alert_manager and (current_time - self.last_voice_time > 4.0):
                if status == "CRITICAL" or in_restricted_zone or any(ac.lower() in label.lower() for ac in ALERT_CLASSES):
                    self.last_voice_time = current_time
                    self.append_log(f"AUDIO OUT: Warning! {label.upper()} approaching in sector.")
                    try:
                        if hasattr(self.alert_manager, 'speak'):
                            self.alert_manager.speak(f"Alert! {label} detected close")
                    except Exception:
                        pass

        self.process_video_recording(annotated_frame)

        self.val_persons.config(text=str(len(self.unique_persons)))
        self.val_vehicles.config(text=str(len(self.unique_vehicles)))
        self.val_trips.config(text=str(self.total_line_crossings))
        self.val_alerts.config(text=str(current_active_alerts))

        return annotated_frame

    def sync_data_to_database(self):
        if not self.database:
            return

        try:
            for obj in self.session_objects.values():
                if hasattr(self.database, 'log_detection'):
                    self.database.log_detection(obj)
                elif hasattr(self.database, 'log_detections'):
                    self.database.log_detections([obj])
                elif hasattr(self.database, 'insert_detection'):
                    self.database.insert_detection(
                        timestamp=obj["last_seen"],
                        track_id=obj["track_id"],
                        label=obj["label"],
                        confidence=obj["max_confidence"],
                        distance=obj["min_distance"],
                        status=obj["status"]
                    )
        except Exception as e:
            print(f"[DATABASE SYNC ERROR] {e}")

    def update_frame(self):
        if not self.is_running:
            return

        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret and frame is not None:
                processed_frame = self.process_detection_pipeline(frame)

                rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_image)

                lbl_w = self.video_label.winfo_width()
                lbl_h = self.video_label.winfo_height()
                if lbl_w > 10 and lbl_h > 10:
                    pil_img = pil_img.resize((lbl_w, lbl_h), Image.Resampling.LANCZOS)

                imgtk = ImageTk.PhotoImage(image=pil_img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

        if self.is_running:
            self.root.after(30, self.update_frame)

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        if self.voice_enabled:
            self.voice_button.config(text="🔊 VOICE ALERT : ON", bg="#0284C7")
            self.append_log("SYSTEM: Voice alerts enabled.")
        else:
            self.voice_button.config(text="🔇 VOICE ALERT : OFF", bg="#64748B")
            self.append_log("SYSTEM: Voice alerts disabled.")

    def export_pdf(self):
        self.sync_data_to_database()
        try:
            if self.report_generator:
                session_data = list(self.session_objects.values())
                try:
                    path = self.report_generator.export_pdf(session_data)
                except TypeError:
                    path = self.report_generator.export_pdf()

                messagebox.showinfo("PDF Executive Report", f"PDF Report Generated Successfully:\n\n{path}")
                self.append_log(f"REPORT: Executive PDF generated cleanly at {path}")
            else:
                messagebox.showwarning("Warning", "Report Generator module missing.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def export_excel(self):
        self.sync_data_to_database()
        try:
            if self.report_generator:
                session_data = list(self.session_objects.values())
                try:
                    path = self.report_generator.export_excel(session_data)
                except TypeError:
                    path = self.report_generator.export_excel()

                messagebox.showinfo("Excel Report", f"Excel Report Generated Successfully:\n\n{path}")
                self.append_log(f"REPORT: Excel exported cleanly at {path}")
            else:
                messagebox.showwarning("Warning", "Report Generator module missing.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def export_csv(self):
        self.sync_data_to_database()
        try:
            if self.report_generator:
                session_data = list(self.session_objects.values())
                try:
                    path = self.report_generator.export_csv(session_data)
                except TypeError:
                    path = self.report_generator.export_csv()

                messagebox.showinfo("CSV Telemetry Logs", f"CSV Telemetry Logs Exported Successfully:\n\n{path}")
                self.append_log(f"REPORT: Telemetry CSV exported at {path}")
            else:
                messagebox.showwarning("Warning", "Report Generator module missing.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def shutdown(self):
        if not self.is_running:
            return

        if messagebox.askyesno("Shutdown", "Do you really want to stop the AI System?"):
            self.append_log("SYSTEM: Emergency Shutdown Initiated.")
            self.is_running = False
            
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None

            if self.camera and self.camera.isOpened():
                self.camera.release()
            cv2.destroyAllWindows()
            self.root.destroy()

    def run(self):
        self.append_log("SYSTEM: Multi Scope Object Detection Engine Initialized.")
        self.root.after(100, self.update_frame)
        self.root.mainloop()

if __name__ == "__main__":
    app = Dashboard()
    app.run()