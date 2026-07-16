import os
import requests
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Saxta Server (Render-in xəta verməməsi və portu tapması üçün)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Agent 24/7 is Live!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8884527838:AAEOF-Kld6tnTCSKcu2tkJO10yTsfslyNX4")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def process_task(user_text):
    return f"✅ Tapşırıq qəbul edildi:\n*{user_text}*\n\n[Sistem: AI mühərriki ilə əlaqə qurulur...]"

def main():
    print("Agent Bulud Sistemində 7/24 Rejimdə İşe Düşdü...", flush=True)
    offset = None
    while True:
        try:
            url = f"{BASE_URL}/getUpdates"
            response = requests.get(url, params={"timeout": 30, "offset": offset}).json()
            
            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        
                        if text == "/start":
                            send_message(chat_id, "Salam! Mən sənin 7/24 Avtonom Agentinəm. İşə hazıram!")
                        else:
                            send_message(chat_id, "⚙️ Gözləyin, işləyirəm...")
                            result = process_task(text)
                            send_message(chat_id, result)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    # Saxta serveri arxa planda işə salırıq ki, Render sakitləşsin
    threading.Thread(target=run_dummy_server, daemon=True).start()
    main()
