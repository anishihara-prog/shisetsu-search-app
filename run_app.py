import subprocess
import sys
import os
import webbrowser

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "app.py")

    # Streamlit を起動
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", app_path])

    # ブラウザを開く
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    main()