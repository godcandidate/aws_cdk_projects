# System Monitoring Dashboard

This project is a real-time system monitoring dashboard built using Python, Dash, and Plotly. It tracks and visualizes CPU, RAM, and Disk usage on a continuous basis, providing both graphical insights and live metrics.

## Features

- **Real-Time Graphs**: Displays live line charts for CPU, RAM, and Disk usage.
- **Configurable View**: Choose between a single combined graph or separate graphs for each metric.
- **Live Metric Display**: Shows current usage percentages for CPU, RAM, and Disk at the top of the dashboard.
- **Auto-Refresh**: Updates every 5 seconds to provide up-to-date metrics.

## Requirements

- Python 3.x
- Dash
- Plotly
- Psutil

Install dependencies with:
```bash
pip install dash plotly psutil
```

## Run App
```bash
  python app.py one 
# python app.py multiple
```