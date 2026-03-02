# Classroom_assistant
# 🧠 AI-Powered Interactive Learning Assistant for Classrooms

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

> A lightweight, offline-capable AI teaching assistant that listens to your questions — and explains them like a friendly tutor.

---

## 🚀 Features

- 🎤 Voice and 💬 text input support
- 🧑‍🏫 Educational, student-friendly answers
- 🧠 Uses `flan-alpaca-base` for question-answering
- 🧩 Modular design (easy to plug in face/visual input)
- 🛑 Smart fallback when model is unsure
- 💻 Runs on low-resource systems (8GB RAM)

---

## 📌 Problem Statement

Modern classrooms lack personalized, real-time help. Students hesitate to ask questions, and teachers can't address everyone. This assistant provides:
- 24/7 intelligent support
- Multimodal input (voice/text)
- Clear, accurate explanations
- Room for future emotion/visual feedback

---

## 🧰 Technologies Used

| Component | Tool |
|----------|------|
| NLP Model | [`declare-lab/flan-alpaca-base`](https://huggingface.co/declare-lab/flan-alpaca-base) |
| Framework | Hugging Face Transformers, PyTorch |
| Voice Input | Python SpeechRecognition |
| Interface | Terminal-based (CLI) |
| System Requirements | Python 3.9+, 8 GB RAM, microphone |

---

## 📁 Project Structure

```
.
├── assistant/                # Core assistant modules
│   ├── core.py              # Main logic controller
│   ├── models.py            # Model loading & response generation
│   ├── interface.py         # UI logic (CLI or future GUI)
│   ├── engagement.py        # Engagement analysis (optional/extendable)
├── main.py                  # Entry point
├── requirements.txt         # Project dependencies
├── .gitignore               # Files/folders to ignore in Git
├── README.md                # Project documentation
├── ai_config.json           # Optional model configuration
├── student_profile.json     # Optional student profile
├── demo_screenshot.png      # Screenshot of the assistant
├── docs/                    # Docs and presentation files
│   ├── AI_Assistant_Report.docx
│   └── AI_Assistant_Presentation.pptx
```

## 👨‍💻 Contributors

| Name             | Role                         | GitHub Username     |
|------------------|------------------------------|---------------------|
| Dharun A         | Lead Developer, Integrator   | `@dharun-anandhan`  |
| Saravanakumar B  | Voice Input, UI Integration  | `@sarvx-gh`|
| Rahul Ramana V   | Testing, Debugging, Docs     | `@rahul-ramana`|

---

## 🎬 Demo Video

> 🔗 Demo Video : (https://www.mediafire.com/file/gtr2h6w4rpiajxf/Intel+Demo+Video.mp4/file)

---

## 🛠️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/classroom-assistant.git
cd classroom-assistant

# 2. Create virtual environment
python -m venv classroom_env
source classroom_env/bin/activate  # Or use Scripts\\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the assistant
python main.py

