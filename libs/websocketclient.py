import queue
import threading
import time
import websocket
import json
import numpy as np
import pandas as pd

class WebSocketClient:
    
    def __init__(self, url, callback):
        self.url = url
        self.ws = None
        self.callback = callback
        self.thread = None

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.ws.close()

    def kill(self):
        self.thread.join(timeout=1)

    def on_message(self, ws, message):
        self.callback(ws, message)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed {close_msg}")

    def on_open(self, ws):
        print("WebSocket opened")

class WebSocketCollector:
    def __init__(self, url:str, max_messages:int=50):
        self.url = url
        self.max_messages = max_messages
        self.queue = queue.Queue()
        self.received = 0
        self.client = WebSocketClient(self.url, self.on_message)

    def on_message(self, ws, message):
        self.queue.put(message)
        self.received += 1
        if self.received >= self.max_messages:
            self.client.close()

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")

    def collect(self):
        self.client.start()

        while self.received < self.max_messages:
            time.sleep(0.1)

        self.client.kill()
        return self.queue
    

class SensorStream:

    def __init__(self, message_queue):
        self.raw_queue = list(message_queue.queue)
        self.init_messages = []
        self.queue = []
        self.size = 0
        self.sensor_informations = {}
        self.sensor_values = {}

        self._processs_sensor_information()
        pass

    def _processs_sensor_information(self):

        for message in self.raw_queue:
            message = json.loads(message)
            if message.get('type')=='initial_state':
                self.init_messages.append(message)
            else:
                self.queue.append(message)

        raw_sensors_array = self.init_messages[0]['data']['sensors']

        for sensor in raw_sensors_array:
            sensor_id = sensor.get('id')
            self.sensor_informations[sensor_id] = {
                "name": sensor.get('name'),
                "type": sensor.get('type'),
                "min": sensor.get("min_value"),
                "max": sensor.get("max_value"),
            }

            self.sensor_values[sensor_id] = {
                "values": [],
                "actual_values": []
            }

        for message in self.queue:
            data = message['data']
            sensor_id = data.get('sensor_id')
            if sensor_id in self.sensor_values:
                self.sensor_values[sensor_id]['values'].append(data.get('value'))
                self.sensor_values[sensor_id]['actual_values'].append(data.get('actual_value'))

        self.size = len(self.queue)

    def print_init_message(self):
        print(json.dumps(self.init_messages, indent=4, sort_keys=True))

    def describe(self):
        print(json.dumps(self.sensor_informations, indent=4, sort_keys=True))

    def print_values(self):
        print(json.dumps(self.sensor_values, indent=4))

    def get_as_dataframe(self) -> pd.DataFrame:
        keys = list(self.sensor_informations.keys())
        columns = np.array([[self.sensor_informations[id].get("name"), f"Actual_{self.sensor_informations[id].get("name")}"] for id in keys])
        dataframe = pd.DataFrame(columns=columns.flatten())
        for i in range(self.size-1):
            row = []
            for key in keys:
                temp_values = self.sensor_values[key].get("values")
                if i < len(temp_values):
                    row.append(self.sensor_values[key].get("values")[i])
                    row.append(self.sensor_values[key].get("actual_values")[i])
                else:
                    row.append(None)
                    row.append(None)
            dataframe.loc[i] = row

        return dataframe

