import tkinter as tk
from assistant.core import ClassroomAssistant
from assistant.interface import ClassroomUI
import logging
import os
from datetime import datetime

def configure_logging():
    """Set up comprehensive logging"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"{log_dir}/assistant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    
    try:
        root = tk.Tk()
        root.title("AI Teaching Assistant")
        root.geometry("1200x800")
        
        # Center window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        root.geometry(f"1200x800+{x}+{y}")
        
        logger.info("Initializing AI Teaching Assistant...")
        assistant = ClassroomAssistant()
        ui = ClassroomUI(root, assistant)
        
        def on_closing():
            logger.info("Closing application...")
            ui.cleanup()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        logger.info("Starting main application loop")
        root.mainloop()
        
    except ImportError as e:
        logger.critical(f"Missing dependency: {e}")
        print(f"ERROR: Please install required packages - {e}")
    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
        print(f"CRITICAL ERROR: {type(e).__name__}: {e}")
    finally:
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()