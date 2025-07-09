# core.py — Cleaned to remove personalization and profile dependencies

import logging
from datetime import datetime
from typing import Dict, Any
import threading
import time
from .models import AIModels
from .engagement import EngagementDetector

class ClassroomAssistant:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.models = AIModels()
        except Exception as e:
            self.logger.critical(f"Failed to initialize AI models: {e}")
            raise RuntimeError("Failed to initialize AI models") from e

        self.engagement_detector = EngagementDetector()
        self._voice_lock = threading.Lock()
        self._processing_lock = threading.Lock()

    def process_query(self, query: str) -> Dict[str, Any]:
        if not query or len(query.strip()) < 2:
            return self._format_response("Please ask a complete question", success=False)

        try:
            with self._processing_lock:
                start_time = time.time()

                response_text = self.models.generate_educational_response(query)
                processing_time = time.time() - start_time
                engagement = self.engagement_detector.last_status

                return self._format_response(response_text, engagement)

        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            return self._format_response("I'm having technical difficulties. Please try again later.", success=False)

    def _format_response(self, text: str, engagement: str = None, success: bool = True) -> Dict[str, Any]:
        response = {
            'text': text,
            'timestamp': datetime.now().isoformat(),
            'engagement': engagement or "neutral",
            'success': success
        }

        if engagement == "Struggling":
            response['tips'] = [
                "Try drawing a diagram of this concept",
                "Explain this to a friend in your own words",
                "Find a real-world example of this"
            ]

        return response

    def start_voice_input(self, callback):
        def voice_thread():
            with self._voice_lock:
                try:
                    text = self.models.voice_input()
                    callback(text if text else None)
                except Exception as e:
                    self.logger.error(f"Voice processing error: {e}")
                    callback(None)

        if not self._voice_lock.locked():
            threading.Thread(target=voice_thread, daemon=True).start()

    def interrupt(self):
        self.models.interrupt()

    def clear_conversation(self):
        self.models.clear_history()
        self.logger.info("Conversation history cleared")
