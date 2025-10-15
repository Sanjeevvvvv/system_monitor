# System Monitor ⚙️

A desktop application for Windows that displays real-time system statistics using a graphical interface built with Tkinter and psutil.

## Features

- **CPU Usage:** Percentage, frequency, and live graph.
- **RAM Usage:** Percentage, used/total, and live graph.
- **Disk Usage:** Select disk, percentage, used/total.
- **Battery Status:** Percentage and charging state.
- **Network Speed:** Upload and download rates.
- **System Uptime:** Time since last boot.
- **Custom Refresh Rate:** Choose how often stats update.
- **High Usage Alerts:** Pop-up warnings for CPU, RAM, or Disk above 90%.
- **Error Logging:** Errors are logged to `system_monitor_errors.log`.

## Requirements

- Python 3.7+
- [psutil](https://pypi.org/project/psutil/)

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/system-monitor.git
    cd system-monitor
    ```

2. Install dependencies:
    ```sh
    pip install psutil
    ```

## Usage

Run the application:
```sh
python system_monitor.py
```

## Screenshots

![System Monitor Screenshot](screenshot.png)

## Notes

- Only works on Windows.
- Alerts pop up if CPU, RAM, or Disk usage exceeds 90%.
- Error logs are saved to `system_monitor_errors.log`.

## License

MIT License
