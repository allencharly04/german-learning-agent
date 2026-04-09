"""
launch.py — starts everything with one command
    python launch.py

Starts:
  1. german_vision_server.py (WebSocket + HTTP on ports 8765/8764) — background thread
  2. Streamlit app.py — foreground (this is what you see in the browser)

Stop everything: Ctrl+C
"""

import subprocess
import threading
import sys
import os
import time
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def run_vision_server():
    """Run the vision server in a subprocess (background)."""
    server_path = os.path.join(os.path.dirname(__file__), "german_vision_server.py")
    if not os.path.exists(server_path):
        print("[launcher] german_vision_server.py not found — skipping vision server")
        return
    subprocess.run([sys.executable, server_path])

def main():
    ip = get_local_ip()

    print("=" * 55)
    print("  German Learning Agent — Launcher")
    print("=" * 55)
    print(f"  Learning app  : http://{ip}:8501")
    print(f"  Live camera   : http://{ip}:8764")
    print("  Stop          : Ctrl+C")
    print("=" * 55)

    # Start vision server in background thread
    vision_thread = threading.Thread(target=run_vision_server, daemon=True)
    vision_thread.start()
    print("[launcher] Vision server starting...")

    # Small delay so vision server loads the YOLO model before Streamlit opens
    time.sleep(2)

    # Start Streamlit in foreground
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    print("[launcher] Starting Streamlit app...")
    print()

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.address", "0.0.0.0",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
        ])
    except KeyboardInterrupt:
        print("\n[launcher] Shutting down. Auf Wiedersehen!")

if __name__ == "__main__":
    main()
