import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class ContextKeeperUI:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("ContextKeeper")
        self.window.geometry("700x500")
        
        # Session list
        self.session_listbox = tk.Listbox(self.window, width=30)
        self.session_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.session_listbox.bind('<<ListboxSelect>>', self.on_session_select)
        
        # Content area
        self.content_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=70)
        self.content_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.refresh_sessions()
    
    def refresh_sessions(self):
        self.session_listbox.delete(0, tk.END)
        sessions = self.db.get_recent_sessions(20)
        for session in sessions:
            start = datetime.fromisoformat(session['start']).strftime('%H:%M')
            display = f"{session['name']} ({session['clip_count']} items) - {start}"
            self.session_listbox.insert(tk.END, display)
            # Store session id as attribute
            self.session_listbox.itemconfig(tk.END, {'id': session['id']})
    
    def on_session_select(self, event):
        selection = self.session_listbox.curselection()
        if not selection:
            return
        
        # Get stored session id (simplified - you'd need a mapping)
        idx = selection[0]
        sessions = self.db.get_recent_sessions(20)
        session = sessions[idx]
        
        self.content_text.delete(1.0, tk.END)
        clips = self.db.get_session_clips(session['id'])
        
        for clip in clips:
            time_str = datetime.fromisoformat(clip['timestamp']).strftime('%H:%M:%S')
            self.content_text.insert(tk.END, f"\n{'='*60}\n[{time_str}]\n{clip['content']}\n")
    
    def run(self):
        self.window.mainloop()