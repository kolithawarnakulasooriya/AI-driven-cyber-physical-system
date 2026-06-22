const ws = new WebSocket(`ws://${window.location.host}/ws`);
const sensors = new Map();
const charts = new Map();
const sensorDataPoints = new Map();
const MAX_DATA_POINTS = 100;

ws.onopen = () => console.log("WebSocket connected");
ws.onerror = (error) => console.error("WebSocket error:", error);
ws.onclose = () => console.log("WebSocket closed");

ws.onmessage = async (event) => {
    const message = JSON.parse(event.data);

    switch (message.type) {
        case "initial_state":
            message.data.sensors.forEach(sensorData => {
                sensors.set(sensorData.id, sensorData);
                sensorDataPoints.set(sensorData.id, []);
            });
            updateUI();
            break;

        case "sensor_created":
            sensors.set(message.data.id, message.data);
            sensorDataPoints.set(message.data.id, []);
            updateUI();
            break;

        case "sensor_deleted":
            sensors.delete(message.data.id);
            sensorDataPoints.delete(message.data.id);
            if (charts.has(message.data.id)) {
                charts.get(message.data.id).destroy();
                charts.delete(message.data.id);
            }
            updateUI();
            break;

        case "sensor_started":
            sensors.get(message.data.id).is_running = true;
            updateUI();
            break;

        case "sensor_stopped":
            sensors.get(message.data.id).is_running = false;
            updateUI();
            break;

        case "data":
            if (sensors.has(message.data.sensor_id)) {
                const dataPoints = sensorDataPoints.get(message.data.sensor_id);
                dataPoints.push({
                    value: message.data.value,
                    timestamp: message.data.timestamp
                });
                if (dataPoints.length > MAX_DATA_POINTS) {
                    dataPoints.shift();
                }

                const sensor = sensors.get(message.data.sensor_id);
                sensor.current_value = message.data.value;

                updateChart(message.data.sensor_id);
                updateSensorInfo(message.data.sensor_id);
            }
            break;

        case "recording_started":
            sensors.get(message.data.id).recording = true;
            updateUI();
            break;

        case "recording_stopped":
            sensors.get(message.data.id).recording = false;
            updateUI();
            break;

        case "mqtt_connected":
            updateMQTTStatus(true);
            break;

        case "mqtt_disconnected":
            updateMQTTStatus(false);
            break;

        case "sensor_config_updated":
            sensors.set(message.data.id, message.data);
            updateUI();
            break;
    }
};

function updateUI() {
    const container = document.getElementById("sensors-container");

    if (sensors.size === 0) {
        container.innerHTML = '<div class="empty-state"><p>No sensors yet. Add one to get started!</p></div>';
        return;
    }

    container.innerHTML = "";
    sensors.forEach((sensor, sensorId) => {
        container.appendChild(createSensorCard(sensor, sensorId));
    });
}

function createSensorCard(sensor, sensorId) {
    const card = document.createElement("div");
    card.className = "card sensor-card";

    const statusBadge = sensor.is_running ? "running" : "stopped";
    const statusText = sensor.is_running ? "🔴 Running" : "⚪ Stopped";

    const parameterInfo = sensor.parameters && Object.keys(sensor.parameters).length > 0
        ? Object.entries(sensor.parameters).map(([key, value]) => `
                <div class="info-item">
                    <span class="info-label">${toTitleCase(key)}</span>
                    <span class="info-value">${parseFloat(value).toFixed(2)}</span>
                </div>`).join("")
        : "";

    const customControls = sensor.type === "custom" ? `
            <div class="parameter-controls custom-controls">
                <div class="parameter-control">
                    <label>Actual Value</label>
                    <input type="range" class="form-range actual-slider" data-sensor-id="${sensorId}"
                        min="${sensor.min_value}" max="${sensor.max_value}" step="0.1"
                        value="${sensor.parameters.actual_value ?? ((sensor.min_value + sensor.max_value) / 2)}">
                    <div class="slider-meta">
                        <span class="slider-label">Value:</span>
                        <span class="slider-value actual-value-display">${parseFloat(sensor.parameters.actual_value ?? ((sensor.min_value + sensor.max_value) / 2)).toFixed(2)}</span>
                    </div>
                </div>
                <div class="parameter-control">
                    <label>Tolerance (std dev)</label>
                    <input type="range" class="form-range tolerance-slider" data-sensor-id="${sensorId}"
                        min="0" max="${((sensor.max_value - sensor.min_value) / 2).toFixed(2)}" step="0.1"
                        value="${sensor.parameters.tolerance ?? (((sensor.max_value - sensor.min_value) / 2) / 2)}">
                    <div class="slider-meta">
                        <span class="slider-label">Value:</span>
                        <span class="slider-value tolerance-value-display">${parseFloat(sensor.parameters.tolerance ?? (((sensor.max_value - sensor.min_value) / 2) / 2)).toFixed(2)}</span>
                    </div>
                </div>
                <div class="parameter-control">
                    <label>Min Value</label>
                    <input type="number" class="form-control range-input min-input" data-sensor-id="${sensorId}" value="${sensor.min_value}" step="0.1">
                </div>
                <div class="parameter-control">
                    <label>Max Value</label>
                    <input type="number" class="form-control range-input max-input" data-sensor-id="${sensorId}" value="${sensor.max_value}" step="0.1">
                </div>
                <div class="parameter-control">
                    <label>Interval (seconds)</label>
                    <input type="number" class="form-control interval-input" data-sensor-id="${sensorId}" value="${sensor.interval}" min="0.1" step="0.1">
                </div>
                <button type="button" class="btn btn-sm btn-outline-primary apply-range-btn d-none" data-sensor-id="${sensorId}">Save Range</button>
            </div>
        ` : `
            <div class="parameter-controls">
                <div class="parameter-control">
                    <label>Interval (seconds)</label>
                    <input type="number" class="form-control interval-input" data-sensor-id="${sensorId}" value="${sensor.interval}" min="0.1" step="0.1">
                </div>
            </div>
        `;

    card.innerHTML = `
        <div class="card-body">
            <div class="sensor-header">
                <h5 class="sensor-title">${sensor.name}</h5>
                <span class="sensor-status-badge ${statusBadge}">${statusText}</span>
            </div>

            <div class="sensor-controls">
                <button class="btn btn-sm btn-success start-btn" data-sensor-id="${sensorId}" ${sensor.is_running ? "disabled" : ""}>Start</button>
                <button class="btn btn-sm btn-danger stop-btn" data-sensor-id="${sensorId}" ${!sensor.is_running ? "disabled" : ""}>Stop</button>
                <button class="btn btn-sm btn-info record-btn" data-sensor-id="${sensorId}">
                    ${sensor.recording ? "Stop Recording" : "Record"}
                </button>
                <button class="btn btn-sm btn-warning delete-btn" data-sensor-id="${sensorId}">Delete</button>
            </div>

            <div class="sensor-info">
                <div class="info-item">
                    <span class="info-label">Type</span>
                    <span class="info-value">${sensor.type}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Current Value</span>
                    <span class="info-value current-value" data-sensor-id="${sensorId}">${sensor.current_value.toFixed(2)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Range</span>
                    <span class="info-value range-value" data-sensor-id="${sensorId}">${sensor.min_value.toFixed(1)} - ${sensor.max_value.toFixed(1)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Interval</span>
                    <span class="info-value">${sensor.interval}s</span>
                </div>
                ${parameterInfo}
            </div>

            ${customControls}

            <div class="chart-container">
                <canvas id="chart-${sensorId}"></canvas>
            </div>
        </div>
    `;

    card.querySelector(".start-btn").addEventListener("click", () => startSensor(sensorId));
    card.querySelector(".stop-btn").addEventListener("click", () => stopSensor(sensorId));
    card.querySelector(".delete-btn").addEventListener("click", () => deleteSensor(sensorId));
    card.querySelector(".record-btn").addEventListener("click", () => toggleRecording(sensorId));

    const intervalInput = card.querySelector(".interval-input");
    if (intervalInput) {
        intervalInput.addEventListener("change", (e) => updateInterval(sensorId, e.target.value));
    }

    if (sensor.type === "custom") {
        const actualSlider = card.querySelector(".actual-slider");
        const toleranceSlider = card.querySelector(".tolerance-slider");
        const actualDisplay = card.querySelector(".actual-value-display");
        const toleranceDisplay = card.querySelector(".tolerance-value-display");
        const minInput = card.querySelector(".min-input");
        const maxInput = card.querySelector(".max-input");
        const applyBtn = card.querySelector(".apply-range-btn");

        const updateSliderLimits = () => {
            const minValue = parseFloat(minInput.value);
            const maxValue = parseFloat(maxInput.value);
            const maxTolerance = Math.max(0, (maxValue - minValue) / 2);

            actualSlider.min = minValue;
            actualSlider.max = maxValue;
            actualSlider.value = Math.min(maxValue, Math.max(minValue, parseFloat(actualSlider.value)));
            actualDisplay.textContent = parseFloat(actualSlider.value).toFixed(2);

            toleranceSlider.max = maxTolerance.toFixed(2);
            toleranceSlider.value = Math.min(maxTolerance, parseFloat(toleranceSlider.value));
            toleranceDisplay.textContent = parseFloat(toleranceSlider.value).toFixed(2);
        };

        updateSliderLimits();

        const showApplyButton = () => applyBtn.classList.remove("d-none");

        const debouncedConfigUpdate = debounce((id, updates) => updateSensorConfig(id, updates), 150);

        actualSlider.addEventListener("input", (e) => {
            actualDisplay.textContent = parseFloat(e.target.value).toFixed(2);
            debouncedConfigUpdate(sensorId, { parameters: { actual_value: parseFloat(e.target.value) } });
        });

        toleranceSlider.addEventListener("input", (e) => {
            toleranceDisplay.textContent = parseFloat(e.target.value).toFixed(2);
            debouncedConfigUpdate(sensorId, { parameters: { tolerance: parseFloat(e.target.value) } });
        });

        minInput.addEventListener("input", showApplyButton);
        maxInput.addEventListener("input", showApplyButton);

        applyBtn.addEventListener("click", () => {
            const minValue = parseFloat(minInput.value);
            const maxValue = parseFloat(maxInput.value);
            if (minValue >= maxValue) {
                alert("Min value must be smaller than max value.");
                return;
            }
            updateSensorConfig(sensorId, {
                min_value: minValue,
                max_value: maxValue
            });
            applyBtn.classList.add("d-none");
        });
    }

    // Create chart after a small delay to ensure DOM is ready
    setTimeout(() => createChart(sensorId, sensor), 100);

    return card;
}

function createChart(sensorId, sensor) {
    const ctx = document.getElementById(`chart-${sensorId}`);
    if (!ctx) return;

    if (charts.has(sensorId)) {
        charts.get(sensorId).destroy();
    }

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: sensor.name,
                data: [],
                borderColor: "#0d6efd",
                backgroundColor: "rgba(13, 110, 253, 0.1)",
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 2,
                pointBackgroundColor: "#0d6efd"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: sensor.min_value,
                    max: sensor.max_value,
                    ticks: {
                        precision: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                }
            }
        }
    });

    charts.set(sensorId, chart);
}

function updateChart(sensorId) {
    const chart = charts.get(sensorId);
    if (!chart) return;

    const sensor = sensors.get(sensorId);
    if (sensor) {
        chart.options.scales.y.min = sensor.min_value;
        chart.options.scales.y.max = sensor.max_value;
    }

    const dataPoints = sensorDataPoints.get(sensorId);
    const labels = dataPoints.map((_, idx) => idx.toString());
    const values = dataPoints.map(d => d.value);

    chart.data.labels = labels;
    chart.data.datasets[0].data = values;
    chart.update('none');
}

function updateSensorInfo(sensorId) {
    const sensor = sensors.get(sensorId);
    if (!sensor) return;

    const valueNode = document.querySelector(`.current-value[data-sensor-id="${sensorId}"]`);
    const rangeNode = document.querySelector(`.range-value[data-sensor-id="${sensorId}"]`);
    if (valueNode) {
        valueNode.textContent = sensor.current_value.toFixed(2);
    }
    if (rangeNode) {
        rangeNode.textContent = `${sensor.min_value.toFixed(1)} - ${sensor.max_value.toFixed(1)}`;
    }
}

async function startSensor(sensorId) {
    await fetch(`/api/sensors/${sensorId}/start`, { method: "POST" });
}

async function stopSensor(sensorId) {
    await fetch(`/api/sensors/${sensorId}/stop`, { method: "POST" });
}

async function deleteSensor(sensorId) {
    if (!confirm("Are you sure you want to delete this sensor?")) return;
    await fetch(`/api/sensors/${sensorId}`, { method: "DELETE" });
}

async function toggleRecording(sensorId) {
    const sensor = sensors.get(sensorId);
    if (sensor.recording) {
        const response = await fetch(`/api/recording/stop/${sensorId}`, { method: "POST" });
        const data = await response.json();
        alert(`Recording saved: ${data.filename}`);
    } else {
        await fetch(`/api/recording/start/${sensorId}`, { method: "POST" });
    }
}

async function updateInterval(sensorId, interval) {
    await fetch(`/api/sensors/${sensorId}/config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: parseFloat(interval) })
    });
}

async function updateSensorConfig(sensorId, updates) {
    await fetch(`/api/sensors/${sensorId}/config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates)
    });
}

function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

function toTitleCase(text) {
    return text.replace(/_/g, " ").replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
}

function updateMQTTStatus(connected) {
    const indicator = document.getElementById("mqtt-indicator");
    if (connected) {
        indicator.textContent = "MQTT: Connected";
        indicator.className = "badge bg-success";
    } else {
        indicator.textContent = "MQTT: Disconnected";
        indicator.className = "badge bg-danger";
    }
}

document.getElementById("sensor-type").addEventListener("change", () => {
    const customFields = document.querySelector(".custom-sensor-params");
    if (document.getElementById("sensor-type").value === "custom") {
        customFields.classList.remove("d-none");
    } else {
        customFields.classList.add("d-none");
    }
});

document.getElementById("add-sensor-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const sensorType = document.getElementById("sensor-type").value;
    const sensorData = {
        name: document.getElementById("sensor-name").value,
        sensor_type: sensorType,
        min_value: parseFloat(document.getElementById("min-value").value),
        max_value: parseFloat(document.getElementById("max-value").value),
        interval: parseFloat(document.getElementById("interval").value),
        parameters: {}
    };

    if (sensorType === "custom") {
        sensorData.parameters = {
            actual_value: parseFloat(document.getElementById("actual-value").value),
            tolerance: parseFloat(document.getElementById("tolerance").value)
        };
    }

    const response = await fetch("/api/sensors", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sensorData)
    });

    if (response.ok) {
        document.getElementById("add-sensor-form").reset();
        document.querySelector(".custom-sensor-params").classList.add("d-none");
    }
});

document.getElementById("mqtt-connect-btn").addEventListener("click", async () => {
    const config = {
        hostname: document.getElementById("mqtt-host").value,
        port: parseInt(document.getElementById("mqtt-port").value),
        topic_prefix: document.getElementById("mqtt-prefix").value
    };

    const response = await fetch("/api/mqtt/connect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config)
    });

    if (!response.ok) {
        alert("Failed to connect to MQTT broker");
    }
});

document.getElementById("mqtt-disconnect-btn").addEventListener("click", async () => {
    await fetch("/api/mqtt/disconnect", { method: "POST" });
});
