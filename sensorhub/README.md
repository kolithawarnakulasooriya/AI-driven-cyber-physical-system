# Sensor Simulation Dashboard

A Python web application for simulating IoT sensors with real-time data generation, live dashboard visualization, MQTT integration, and CSV data recording.

## Features

✅ **Sensor Management**
- Add/remove sensors dynamically
- Multiple sensor types: Gaussian (Temperature/Humidity), Wave (Pressure/Flow), Random Walk (Energy/Power), LIDAR (Distance), Custom patterns
- Configure sensor parameters (name, min/max values, generation interval)
- Start/stop sensor data generation
- Real-time parameter updates

✅ **Real-time Dashboard**
- WebSocket-based live updates
- Chart.js visualization with 100+ data points per sensor
- Current, min, max value displays
- Multiple sensors on one page
- Status indicators for running/stopped/recording states

✅ **Background Data Generation**
- Asyncio-based continuous data generation
- Mathematically sound sensor data:
  - **Gaussian**: Normal distribution with configurable mean, std-dev, and drift
  - **Wave**: Sine/cosine patterns with noise overlay
  - **Random Walk**: Brownian motion with trend components
  - **LIDAR**: Distance measurements with bounds checking
  - **Custom**: User-defined linear/exponential/random patterns

✅ **CSV Recording**
- Record sensor data to CSV files with timestamps
- Start/stop recording per sensor
- Download recorded files
- Data written continuously (not buffered)

✅ **MQTT Integration**
- Connect to MQTT broker
- Publish sensor data to `sensors/{sensor_id}/{sensor_type}` topics
- Connection status indicator
- Configurable broker settings

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python app.py
```

Then open your browser to: **http://localhost:8000**

## Usage

### Adding Sensors

1. Fill in the "Add New Sensor" form:
   - **Sensor Name**: e.g., "Room Temperature"
   - **Sensor Type**: Choose from 5 types
   - **Min/Max Values**: Define the range
   - **Interval**: Time between readings (seconds)

2. Click "Add Sensor"

### Controlling Sensors

- **Start**: Begin data generation
- **Stop**: Pause data generation
- **Record**: Start/stop CSV recording
- **Delete**: Remove the sensor

### Recording Data

1. Click "Record" on any running sensor
2. Sensor data will be written to `recordings/` directory
3. Click "Stop Recording" to finish
4. A download link will appear

### MQTT Setup

1. Enter MQTT broker details (hostname, port, topic prefix)
2. Click "Connect to MQTT"
3. The indicator will change to "Connected" when successful
4. Data will be published to MQTT topics automatically

## Project Structure

```
sensor-sim-app/
├── app.py                    # FastAPI main application
├── requirements.txt          # Python dependencies
├── static/
│   ├── index.html           # Dashboard UI
│   ├── style.css            # Styling
│   └── dashboard.js         # Frontend WebSocket & charts
├── models/
│   └── sensor.py            # Sensor data models
├── generators/
│   ├── base.py              # Abstract generator class
│   ├── gaussian.py          # Gaussian distribution
│   ├── wave.py              # Wave pattern generator
│   ├── random_walk.py       # Random walk generator
│   └── custom.py            # Custom pattern generator
├── integrations/
│   ├── mqtt_handler.py      # MQTT client
│   └── csv_recorder.py      # CSV writing
└── recordings/              # Generated CSV files
```

## API Endpoints

### REST API

- `POST /api/sensors` - Create sensor
- `DELETE /api/sensors/{id}` - Delete sensor
- `GET /api/sensors` - List all sensors
- `POST /api/sensors/{id}/start` - Start sensor
- `POST /api/sensors/{id}/stop` - Stop sensor
- `POST /api/sensors/{id}/config` - Update configuration
- `POST /api/recording/start/{id}` - Start CSV recording
- `POST /api/recording/stop/{id}` - Stop recording
- `GET /api/recordings/download/{filename}` - Download CSV
- `POST /api/mqtt/connect` - Connect to MQTT
- `POST /api/mqtt/disconnect` - Disconnect MQTT

### WebSocket

- **Endpoint**: `ws://localhost:8000/ws`
- **Events**: Real-time sensor data, status updates, MQTT events

## Sensor Type Details

### Gaussian (Temperature/Humidity)
- Generates normally distributed values
- **Parameters**: `mean`, `std_dev`, `drift`
- **Use case**: Temperature, humidity sensors

### Wave (Pressure/Flow)
- Generates sine wave with noise
- **Parameters**: `frequency`, `amplitude`, `offset`, `noise_level`
- **Use case**: Pressure, flow rate, oscillating sensors

### Random Walk (Energy/Power)
- Generates Brownian motion path
- **Parameters**: `step_size`, `trend`
- **Use case**: Energy consumption, gradual changes

### LIDAR (Distance)
- Similar to random walk with bounds checking
- **Use case**: Distance measurements, object detection

### Custom
- User-defined patterns (linear, exponential, random)
- **Parameters**: `pattern`, `total_steps`, `noise_level`
- **Use case**: Testing specific scenarios

## Example: Temperature Sensor

```bash
curl -X POST http://localhost:8000/api/sensors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Room Temperature",
    "sensor_type": "gaussian",
    "min_value": 15,
    "max_value": 30,
    "interval": 1.0,
    "parameters": {
      "mean": 22,
      "std_dev": 2,
      "drift": 0.01
    }
  }'
```

## Performance Notes

- Tested with 5+ simultaneous sensors
- Data is kept in-memory (last 1000 points per sensor)
- WebSocket updates sent at data generation interval
- CSV writing is non-blocking
- MQTT publishing is non-blocking

## Browser Compatibility

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Notes

- Data is cleared on application restart (in-memory storage)
- CSV files persist in the `recordings/` directory
- MQTT integration is optional (works without a broker)
- All sensor data is generated locally; no external API calls

## Future Enhancements

- Database persistence (PostgreSQL)
- Data export formats (JSON, Parquet)
- Advanced charting options (3D, heatmaps)
- Sensor scheduling and automation
- Historical data analysis
- Multi-user support

## License

MIT
