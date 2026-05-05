import time
import pyperclip
from threading import Thread
from storage import ContextKeeperDB

class ClipboardMonitor:
    def __init__(self, db):
        self.db = db
        self.last_content = ""
        self.running = True
        # Create a separate DB connection for this thread
        self.thread_db = ContextKeeperDB("contextkeeper.db")
    
    def start(self):
        def monitor_loop():
            while self.running:
                try:
                    content = pyperclip.paste()
                    if content and content != self.last_content:
                        if len(content) < 50000:
                            # Use thread-specific DB connection
                            self.thread_db.add_clip(content)
                            self.last_content = content
                            print(f"[Saved] {content[:80]}...")
                except Exception as e:
                    print(f"Monitor error: {e}")
                time.sleep(0.5)
        
        thread = Thread(target=monitor_loop, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        self.running = False  # Changed from True to False
        if hasattr(self, 'thread_db'):
            self.thread_db.close()