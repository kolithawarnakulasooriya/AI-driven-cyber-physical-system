# SensorHub Study Guide

## Overview
SensorHub is a Python-based sensor simulation dashboard that enables real-time generation, visualization, and recording of IoT sensor data. It supports multiple sensor types and integrates with MQTT for distributed architectures.

## Features
- **Sensor Management**: Add/remove various sensor types (Gaussian, Wave, Random Walk, LIDAR, Custom).
- **Real-time Dashboard**: Live visualization using Chart.js with extensive data points.
- **Background Data Generation**: Asynchronous, mathematically accurate sensor data generation.
- **CSV Recording**: Continuous data recording to CSV files with timestamps.
- **MQTT Integration**: Optional broker integration for publish/subscribe architectures.
- **WebSocket API**: Real-time updates via WebSocket connections.

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application:
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   or simply `python app.py`.
4. Access the dashboard at `http://localhost:8000`.

## Usage
### Adding Sensors
- Fill out the "Add New Sensor" form with name, type, min/max values, interval, and parameters.
- Click "Add Sensor".

### Controlling Sensors
- Use "Start", "Stop", "Record", and "Delete" actions to control sensor behavior.

### Recording Data
- Click "Record" on a running sensor, then "Stop Recording" to finish. Download the CSV file.

### MQTT Setup
- Enter broker details (hostname, port, topic prefix) and connect.

## Sensor Types
- **Gaussian**: Normal distribution with configurable mean, std dev, drift.
- **Wave**: Sine/cosine patterns with noise.
- **Random Walk**: Brownian motion with trend.
- **LIDAR**: Distance measurements with bounds checking.
- **Custom**: User-defined patterns (linear, exponential, random).

## API Endpoints
- `POST /api/sensors` - Create sensor
- `DELETE /api/sensors/{id}` - Delete sensor
- `GET /api/sensors` - List sensors
- `POST /api/sensors/{id}/start` - Start sensor
- `POST /api/sensors/{id}/stop` - Stop sensor
- `POST /api/recording/start/{id}` - Start CSV recording
- `POST /api/recording/stop/{id}` - Stop recording
- `GET /api/recordings/download/{filename}` - Download CSV
- `POST /api/mqtt/connect` - Connect to MQTT
- `POST /api/mqtt/disconnect` - Disconnect MQTT

## Performance & Compatibility
- Tested with 5+ simultaneous sensors.
- In-memory storage (data cleared on restart).
- Supports Chrome, Firefox, Safari, Edge.

## License
MIT