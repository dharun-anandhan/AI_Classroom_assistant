import cv2
import numpy as np
import logging
from datetime import datetime
from typing import Dict, Any

class EngagementDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emotion_map = {
            0: {'icon': '😊', 'state': 'Engaged', 'color': '#4CAF50'},
            1: {'icon': '🤔', 'state': 'Thinking', 'color': '#FFC107'},
            2: {'icon': '😕', 'state': 'Confused', 'color': '#FF9800'},
            3: {'icon': '😞', 'state': 'Struggling', 'color': '#F44336'},
            4: {'icon': '😐', 'state': 'Neutral', 'color': '#9E9E9E'}
        }
        self.face_cascade = self._load_cascade()
        self.last_status = "Neutral"
        self.engagement_history = []
        
    def _load_cascade(self):
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            cascade = cv2.CascadeClassifier(cascade_path)
            if cascade.empty():
                raise RuntimeError("Failed to load face detection cascade")
            return cascade
        except Exception as e:
            self.logger.error(f"Failed to load face detection: {e}")
            raise RuntimeError("Could not initialize engagement tracking")

    def analyze_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30))
            
            if len(faces) == 0:
                self.last_status = "Neutral"
                return self.emotion_map[4]
            
            (x, y, w, h) = faces[0]
            face_ratio = (w * h) / (frame.shape[0] * frame.shape[1])
            
            if face_ratio > 0.15:
                self.last_status = "Engaged"
                result = self.emotion_map[0]
            elif face_ratio > 0.08:
                self.last_status = "Thinking"
                result = self.emotion_map[1]
            else:
                self.last_status = "Struggling"
                result = self.emotion_map[3]
                
            self._record_engagement(result['state'])
            return result
            
        except Exception as e:
            self.logger.error(f"Engagement analysis failed: {e}")
            return self.emotion_map[4]

    def _record_engagement(self, state: str):
        self.engagement_history.append({
            "timestamp": datetime.now().isoformat(),
            "state": state
        })
        self.engagement_history = self.engagement_history[-100:]