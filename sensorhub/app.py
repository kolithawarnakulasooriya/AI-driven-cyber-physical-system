from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import asyncio
import json
from typing import Dict, List
from datetime import datetime
import os

from models.sensor import Sensor, SensorConfig, SensorReading
from generators import get_generator
from integrations.mqtt_handler import MQTTHandler
from integrations.csv_recorder import CSVRecorder

app = FastAPI(title="Sensor Simulation Dashboard")

SENSOR_PERSISTENCE_FILE = os.path.join(os.path.dirname(__file__), "sensors.json")

sensors: Dict[str, Sensor] = {}
sensor_tasks: Dict[str, asyncio.Task] = {}
mqtt_handler = MQTTHandler()
csv_recorder = CSVRecorder()
websocket_clients: List[WebSocket] = []

app.mount("/static", StaticFiles(directory="static"), name="static")


def load_sensors_from_file():
    if not os.path.exists(SENSOR_PERSISTENCE_FILE):
        return
    try:
        with open(SENSOR_PERSISTENCE_FILE, "r") as f:
            data = json.load(f)
        for sensor_data in data:
            sensor = Sensor.from_dict(sensor_data)
            sensors[sensor.id] = sensor
    except Exception as e:
        print(f"Failed to load sensors from {SENSOR_PERSISTENCE_FILE}: {e}")


def save_sensors_to_file():
    try:
        with open(SENSOR_PERSISTENCE_FILE, "w") as f:
            json.dump([sensor.to_dict() for sensor in sensors.values()], f, indent=2)
    except Exception as e:
        print(f"Failed to save sensors to {SENSOR_PERSISTENCE_FILE}: {e}")


load_sensors_from_file()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html") as f:
        return f.read()


@app.post("/api/sensors")
async def create_sensor(config: dict):
    try:
        sensor_config = SensorConfig(
            name=config["name"],
            sensor_type=config["sensor_type"],
            interval=config.get("interval", 1.0),
            min_value=config["min_value"],
            max_value=config["max_value"],
            parameters=config.get("parameters", {})
        )
        sensor = Sensor(sensor_config)
        sensors[sensor.id] = sensor
        save_sensors_to_file()

        await broadcast_message({
            "type": "sensor_created",
            "data": sensor.to_dict()
        })

        return {"id": sensor.id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/sensors/{sensor_id}")
async def delete_sensor(sensor_id: str):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    if sensor_id in sensor_tasks:
        sensor_tasks[sensor_id].cancel()
        del sensor_tasks[sensor_id]

    csv_recorder.stop_recording(sensor_id)
    del sensors[sensor_id]
    save_sensors_to_file()

    await broadcast_message({
        "type": "sensor_deleted",
        "data": {"id": sensor_id}
    })

    return {"status": "deleted"}


@app.post("/api/sensors/{sensor_id}/start")
async def start_sensor(sensor_id: str):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]
    sensor.is_running = True

    if sensor_id not in sensor_tasks:
        task = asyncio.create_task(generate_sensor_data(sensor_id))
        sensor_tasks[sensor_id] = task

    await broadcast_message({
        "type": "sensor_started",
        "data": {"id": sensor_id}
    })

    return {"status": "started"}


@app.post("/api/sensors/{sensor_id}/stop")
async def stop_sensor(sensor_id: str):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]
    sensor.is_running = False

    if sensor_id in sensor_tasks:
        sensor_tasks[sensor_id].cancel()
        del sensor_tasks[sensor_id]

    await broadcast_message({
        "type": "sensor_stopped",
        "data": {"id": sensor_id}
    })

    return {"status": "stopped"}


@app.post("/api/sensors/{sensor_id}/config")
async def update_sensor_config(sensor_id: str, updates: dict):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]

    if "interval" in updates:
        sensor.config.interval = updates["interval"]

    if "min_value" in updates or "max_value" in updates:
        min_value = updates.get("min_value", sensor.config.min_value)
        max_value = updates.get("max_value", sensor.config.max_value)
        if min_value >= max_value:
            raise HTTPException(status_code=400, detail="min_value must be less than max_value")
        sensor.config.min_value = min_value
        sensor.config.max_value = max_value

        if "actual_value" in sensor.config.parameters:
            actual = sensor.config.parameters.get("actual_value")
            if actual is not None:
                sensor.config.parameters["actual_value"] = max(min_value, min(max_value, float(actual)))

        if "tolerance" in sensor.config.parameters:
            tolerance = sensor.config.parameters.get("tolerance")
            if tolerance is not None:
                max_tolerance = (max_value - min_value) / 2
                sensor.config.parameters["tolerance"] = min(max_tolerance, float(tolerance))

    if "parameters" in updates:
        sensor.config.parameters.update(updates["parameters"])
        if sensor.config.sensor_type == "custom":
            if "actual_value" in updates["parameters"]:
                actual_value = float(updates["parameters"]["actual_value"])
                sensor.config.parameters["actual_value"] = max(
                    sensor.config.min_value,
                    min(sensor.config.max_value, actual_value)
                )
            if "tolerance" in updates["parameters"]:
                tolerance = float(updates["parameters"]["tolerance"])
                max_tolerance = (sensor.config.max_value - sensor.config.min_value) / 2
                sensor.config.parameters["tolerance"] = max(0.0, min(max_tolerance, tolerance))

    save_sensors_to_file()
    await broadcast_message({
        "type": "sensor_config_updated",
        "data": sensor.to_dict()
    })

    return {"status": "updated"}


@app.post("/api/recording/start/{sensor_id}")
async def start_recording(sensor_id: str):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]
    filename = csv_recorder.start_recording(sensor_id, sensor.config.name)
    sensor.recording = True

    await broadcast_message({
        "type": "recording_started",
        "data": {"id": sensor_id, "filename": filename}
    })

    return {"filename": filename}


@app.post("/api/recording/stop/{sensor_id}")
async def stop_recording(sensor_id: str):
    if sensor_id not in sensors:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor = sensors[sensor_id]
    filename = csv_recorder.stop_recording(sensor_id)
    sensor.recording = False

    await broadcast_message({
        "type": "recording_stopped",
        "data": {"id": sensor_id, "filename": filename}
    })

    return {"filename": filename}


@app.get("/api/recordings/download/{filename}")
async def download_recording(filename: str):
    filepath = os.path.join("recordings", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="text/csv", filename=filename)


@app.post("/api/mqtt/connect")
async def mqtt_connect(config: dict):
    try:
        hostname = config.get("hostname", "localhost")
        port = config.get("port", 1883)
        topic_prefix = config.get("topic_prefix", "sensors")

        success = mqtt_handler.connect(hostname, port, topic_prefix)
        if success:
            await broadcast_message({
                "type": "mqtt_connected",
                "data": {"hostname": hostname, "port": port}
            })
            return {"status": "connected"}
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to MQTT broker")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/mqtt/disconnect")
async def mqtt_disconnect():
    mqtt_handler.disconnect()
    await broadcast_message({
        "type": "mqtt_disconnected",
        "data": {}
    })
    return {"status": "disconnected"}


@app.get("/api/sensors")
async def get_sensors():
    return [sensor.to_dict() for sensor in sensors.values()]


async def generate_sensor_data(sensor_id: str):
    try:
        while True:
            sensor = sensors[sensor_id]
            generator = get_generator(
                sensor.config.sensor_type,
                sensor.config.min_value,
                sensor.config.max_value,
                sensor.config.parameters
            )
            if not sensor.is_running:
                break

            value = generator.generate()
            reading = sensor.add_reading(value, sensor.config.parameters.get("actual_value"))

            if sensor.recording:
                csv_recorder.write_reading(sensor_id, reading.value, reading.actual_value, reading.timestamp)

            if mqtt_handler.is_connected():
                mqtt_handler.publish(
                    sensor_id,
                    sensor.config.sensor_type,
                    value,
                    reading.timestamp.isoformat()
                )

            await broadcast_message({
                "type": "data",
                "data": reading.to_dict()
            })

            await asyncio.sleep(sensor.config.interval)
    except asyncio.CancelledError:
        pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)

    send_initial_data = {
        "type": "initial_state",
        "data": {
            "sensors": [s.to_dict() for s in sensors.values()],
            "mqtt_connected": mqtt_handler.is_connected(),
            "recordings": csv_recorder.get_active_recordings()
        }
    }
    await websocket.send_text(json.dumps(send_initial_data))

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_clients.remove(websocket)


async def broadcast_message(message: dict):
    disconnected = []
    for client in websocket_clients:
        try:
            await client.send_text(json.dumps(message))
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        if client in websocket_clients:
            websocket_clients.remove(client)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
