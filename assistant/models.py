# models.py — FINAL update using `declare-lab/flan-alpaca-base` for educational Q&A

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, GenerationConfig
import logging
import re
import threading
from typing import Optional
import speech_recognition as sr
import time

class AIModels:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._stop_event = threading.Event()
        self._listening = False
        self.tokenizer = None
        self.model = None
        self._initialize_models()
        self.conversation_history = []
        self.max_history = 3

        self.system_prompt = (
            "You are a knowledgeable and friendly teaching assistant."
            " Provide accurate, student-friendly explanations with examples in simple language."
        )

        self.generation_config = GenerationConfig(
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
            num_beams=1,
            early_stopping=True
        )

    def _initialize_models(self):
        try:
            model_name = "declare-lab/flan-alpaca-base"
            self.logger.info(f"Loading model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
        except Exception as e:
            self.logger.error(f"Model initialization failed: {e}")
            raise RuntimeError("Failed to load model")

    def generate_educational_response(self, prompt: str) -> str:
        if not self.model or not self.tokenizer:
            return "System not properly initialized."

        try:
            full_prompt = f"{self.system_prompt}\nQuestion: {prompt}"
            self.logger.info(f"Prompt sent to model: {full_prompt}")

            inputs = self.tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config
            )

            decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            cleaned = re.sub(r'\s+', ' ', decoded)

            self.logger.info(f"Raw model output: {repr(decoded)}")

            if cleaned.lower() in ["", "explain", prompt.lower().strip()] or len(cleaned.split()) < 3:
                return self._get_fallback_response(prompt)

            self.conversation_history.append(f"Student: {prompt}")
            self.conversation_history.append(f"Assistant: {cleaned}")
            return cleaned if cleaned.endswith(('.', '!', '?')) else cleaned + '.'

        except Exception as e:
            self.logger.error(f"Response generation error: {e}")
            return self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt: str = "") -> str:
        if prompt:
            return f"I'm thinking about your question: '{prompt.strip()}'. Could you rephrase it?"
        return "I'm still learning. Could you ask in a different way?"

    def voice_input(self) -> Optional[str]:
        if self._stop_event.is_set() or self._listening:
            return None

        self._listening = True
        self._stop_event.clear()
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("Listening...")
                for _ in range(3):
                    if self._stop_event.is_set():
                        return None
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                        text = recognizer.recognize_google(audio)
                        if text and len(text.strip()) > 3:
                            return text.strip()
                    except Exception:
                        continue
                return None
        except Exception as e:
            self.logger.error(f"Voice input error: {e}")
            return None
        finally:
            self._listening = False

    def interrupt(self):
        self._stop_event.set()
        self.logger.info("Interrupted")

    def clear_history(self):
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
