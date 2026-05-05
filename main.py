#!/usr/bin/env python3
import sys
import signal
from threading import Event

from storage import ContextKeeperDB
from monitor import ClipboardMonitor
from ui import ContextKeeperUI

def main():
    db = ContextKeeperDB()
    monitor = ClipboardMonitor(db)
    
    print("🔍 ContextKeeper is running")
    print("   - Clipboard monitoring active")
    print("   - Opening viewer window")
    
    monitor.start()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n👋 Shutting down...")
        monitor.stop()
        db.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start UI (blocks until window closed)
    ui = ContextKeeperUI(db)
    ui.run()
    
    # Cleanup after UI closes
    monitor.stop()
    db.close()

if __name__ == "__main__":
    main()