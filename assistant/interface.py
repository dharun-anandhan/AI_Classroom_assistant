import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu
from PIL import Image, ImageTk
import cv2
import logging
import threading
import pyttsx3

class ClassroomUI:
    def __init__(self, root, assistant):
        self.root = root
        self.assistant = assistant
        self.voice_active = False
        self.processing = False
        self.cap = self._initialize_webcam()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.setup_ui()
        self.update_webcam()
        self._setup_styles()
        self._create_menu()
        
    def _initialize_webcam(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                logging.warning("Could not open webcam")
                return None
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return cap
        except Exception as e:
            logging.error(f"Webcam error: {e}")
            messagebox.showwarning("Camera Unavailable", "Engagement tracking will be limited without camera access")
            return None

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#f5f7fa')
        style.configure('Header.TFrame', background='#3f51b5')
        style.configure('TLabel', background='#f5f7fa', font=('Segoe UI', 10))
        style.configure('Header.TLabel', background='#3f51b5', foreground='white', font=('Segoe UI', 12, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=6, relief='flat')
        style.configure('Primary.TButton', background='#4CAF50', foreground='white')
        style.configure('Accent.TButton', background='#2196F3', foreground='white')
        style.configure('Warning.TButton', background='#FF9800', foreground='white')
        style.configure('Chat.TFrame', background='white')
        
    def _create_menu(self):
        menubar = Menu(self.root)
        
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Learning Style", command=self._show_learning_style_dialog)
        settings_menu.add_command(label="Difficulty Level", command=self._show_difficulty_dialog)
        settings_menu.add_separator()
        settings_menu.add_command(label="Clear Conversation", command=self.clear_conversation)
        settings_menu.add_command(label="View Profile", command=self._show_profile)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def _show_learning_style_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Learning Style")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Select your preferred learning style:").pack(pady=10)
        
        style_var = tk.StringVar(value=self.assistant.student_profile.get("learning_style", "visual"))
        
        for style in ["visual", "auditory", "kinesthetic"]:
            rb = ttk.Radiobutton(dialog, text=style.capitalize(), variable=style_var, value=style)
            rb.pack(anchor='w', padx=20)
        
        def save():
            self.assistant.update_learning_style(style_var.get())
            dialog.destroy()
            messagebox.showinfo("Success", "Learning style updated successfully")
        
        ttk.Button(dialog, text="Save", command=save, style='Primary.TButton').pack(pady=10)
        
    def _show_difficulty_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Difficulty Level")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Select your current education level:").pack(pady=10)
        
        level_var = tk.StringVar(value=self.assistant.student_profile.get("difficulty_level", "high_school"))
        
        levels = [
            ("Elementary School", "elementary"),
            ("Middle School", "middle_school"),
            ("High School", "high_school"),
            ("College", "college")
        ]
        
        for text, level in levels:
            rb = ttk.Radiobutton(dialog, text=text, variable=level_var, value=level)
            rb.pack(anchor='w', padx=20)
        
        def save():
            self.assistant.update_difficulty_level(level_var.get())
            dialog.destroy()
            messagebox.showinfo("Success", "Difficulty level updated successfully")
        
        ttk.Button(dialog, text="Save", command=save, style='Primary.TButton').pack(pady=10)
        
    def _show_profile(self):
        profile = self.assistant.student_profile
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Student Profile")
        dialog.geometry("400x300")
        
        frame = ttk.Frame(dialog)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Learning Style:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w')
        ttk.Label(frame, text=profile.get("learning_style", "Not set").capitalize()).grid(row=0, column=1, sticky='w')
        
        ttk.Label(frame, text="Difficulty Level:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w')
        ttk.Label(frame, text=profile.get("difficulty_level", "Not set").replace("_", " ").title()).grid(row=1, column=1, sticky='w')
        
        ttk.Label(frame, text="Total Interactions:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w')
        ttk.Label(frame, text=str(len(profile.get("interaction_history", [])))).grid(row=2, column=1, sticky='w')
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

    def _show_help(self):
        messagebox.showinfo(
            "Help",
            "How to use the AI Teaching Assistant:\n\n"
            "1. Type your question in the text box or use the voice button\n"
            "2. Press Send or Enter to get an explanation\n"
            "3. The assistant will speak the answer aloud\n"
            "4. Use Settings menu to customize your learning experience\n"
            "5. The camera tracks your engagement level automatically"
        )

    def setup_ui(self):
        self.root.configure(background='#f5f7fa')
        
        # Header
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="AI Teaching Assistant", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Main content
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        
        # Left panel - Engagement tracking
        left_frame = ttk.Frame(main_frame, width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        
        engagement_frame = ttk.LabelFrame(left_frame, text="Student Engagement", padding=10)
        engagement_frame.pack(fill=tk.BOTH, expand=True)
        
        self.webcam_label = ttk.Label(engagement_frame)
        self.webcam_label.pack()
        
        self.engagement_label = ttk.Label(engagement_frame, text="Status: Analyzing...", font=('Segoe UI', 11), anchor='center')
        self.engagement_label.pack(fill=tk.X, pady=10)
        
        # Right panel - Learning interface
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        chat_frame = ttk.LabelFrame(right_frame, text="Learning Session", padding=10, style='Chat.TFrame')
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat history with scrollbar
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, font=('Segoe UI', 11), padx=15, pady=15, bg='white', relief=tk.FLAT, state='disabled'
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for message styling
        self.chat_history.tag_config('assistant', foreground='#2c3e50')
        self.chat_history.tag_config('user', foreground='#2980b9')
        self.chat_history.tag_config('system', foreground='#7f8c8d')
        self.chat_history.tag_config('error', foreground='#e74c3c')
        
        # Input area
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, pady=(10,0))
        
        self.input_entry = ttk.Entry(input_frame, font=('Segoe UI', 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        self.input_entry.focus_set()
        
        self.voice_btn = ttk.Button(input_frame, text="🎤 Voice", command=self.toggle_voice, style='Accent.TButton')
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_message, style='Primary.TButton')
        self.send_btn.pack(side=tk.LEFT)
        
        # Add initial welcome message
        self.add_message("Assistant", "Welcome to your AI-powered learning session!\nAsk me anything, and I'll provide detailed explanations to help you learn.", 'assistant')
        self.speak("Welcome to your AI-powered learning session! Ask me anything.")

    def speak(self, text: str):
        def speak_thread():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logging.error(f"Text-to-speech failed: {e}")
        
        threading.Thread(target=speak_thread, daemon=True).start()

    def toggle_voice(self):
        if self.voice_active:
            self.voice_active = False
            self.voice_btn.config(text="🎤 Voice")
            self.assistant.interrupt()
            self.add_message("System", "Voice input canceled", 'system')
            return
            
        if self.processing:
            messagebox.showwarning("Processing", "Please wait for current response to complete")
            return
            
        self.voice_active = True
        self.voice_btn.config(text="🔴 Listening...")
        self.add_message("System", "Listening... Please speak clearly into your microphone", 'system')
        self.speak("I'm listening. Please ask your question.")
        
        def callback(transcript):
            self.voice_active = False
            self.voice_btn.config(text="🎤 Voice")
            
            if transcript:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, transcript)
                self.send_message()
            else:
                self.add_message("System", "Couldn't detect speech. Please try speaking louder and clearer.", 'system')
                self.speak("I couldn't hear you. Please try speaking louder.")
        
        threading.Thread(target=lambda: self.assistant.start_voice_input(callback), daemon=True).start()

    def send_message(self):
        if self.processing:
            messagebox.showwarning("Processing", "Please wait for current response to complete")
            return
            
        query = self.input_entry.get().strip()
        if not query:
            return
            
        self.input_entry.delete(0, tk.END)
        self.add_message("You", query, 'user')
        
        self.processing = True
        self.input_entry.config(state='disabled')
        self.voice_btn.config(state='disabled')
        self.send_btn.config(state='disabled')
        
        self.root.after(100, lambda: self.process_query(query))

    def process_query(self, query: str):
        try:
            response = self.assistant.process_query(query)
            
            if response.get('success', False):
                self.add_message("Assistant", response['text'], 'assistant')
                self.speak(response['text'])
                
                if response.get('engagement') == "Struggling":
                    tips = "Learning Tips:\n- " + "\n- ".join(response.get('tips', []))
                    self.add_message("Assistant", tips, 'system')
                    self.speak("Here are some learning tips to help you understand better.")
            else:
                self.add_message("System", response['text'], 'error')
                self.speak("I'm having trouble with that question. Could you try rephrasing it?")
                
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            self.add_message("System", "Sorry, I encountered an error. Please try again.", 'error')
            self.speak("I'm having technical difficulties. Please try again.")
        finally:
            self.processing = False
            self.input_entry.config(state='normal')
            self.voice_btn.config(state='normal')
            self.send_btn.config(state='normal')
            self.input_entry.focus_set()

    def add_message(self, sender: str, text: str, tag: str):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {text}\n\n", tag)
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def update_webcam(self):
        if self.cap:
            try:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.resize(frame, (320, 240))
                    result = self.assistant.engagement_detector.analyze_frame(frame)
                    
                    self.engagement_label.config(
                        text=f"Status: {result['state']} {result['icon']}",
                        foreground=result['color']
                    )
                    
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(img)
                    self.webcam_label.imgtk = ImageTk.PhotoImage(image=img)
                    self.webcam_label.config(image=self.webcam_label.imgtk)
                    
            except Exception as e:
                logging.error(f"Webcam update error: {e}")
        
        self.root.after(100, self.update_webcam)

    def clear_conversation(self):
        self.assistant.clear_conversation()
        self.chat_history.config(state='normal')
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state='disabled')
        self.add_message("Assistant", "Conversation history cleared. What would you like to learn about now?", 'assistant')
        self.speak("Conversation history cleared. What would you like to learn about now?")

    def cleanup(self):
        try:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            self.engine.stop()
        except Exception as e:
            logging.error(f"Cleanup error: {e}")