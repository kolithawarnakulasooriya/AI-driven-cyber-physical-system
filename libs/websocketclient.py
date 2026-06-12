import queue
import threading
import time
import websocket

class WebSocketCollector:
    def __init__(self, url, max_messages=50):
        self.url = url
        self.max_messages = max_messages
        self.queue = queue.Queue()
        self.received = 0
        self.ws = None

    def on_message(self, ws, message):
        self.queue.put(message)
        self.received += 1
        if self.received >= self.max_messages:
            ws.close()

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")

    def collect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()

        while self.received < self.max_messages:
            time.sleep(0.1)

        thread.join(timeout=1)
        return self.queue