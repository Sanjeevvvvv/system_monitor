import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime
import os

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor ⚙️")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#101010")

        # Title
        ttk.Label(self.root, text="🖥️ System Monitor", font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Green.Horizontal.TProgressbar", thickness=20, background="#4CAF50")
        self.style.configure("Yellow.Horizontal.TProgressbar", thickness=20, background="#FFC107")
        self.style.configure("Red.Horizontal.TProgressbar", thickness=20, background="#F44336")

        # Refresh rate
        ttk.Label(self.root, text="Refresh Rate (seconds)").pack()
        self.refresh_rate = tk.DoubleVar(value=1.0)
        self.refresh_dropdown = ttk.Combobox(self.root, values=[0.5, 1, 2, 5], textvariable=self.refresh_rate, state="readonly", width=10)
        self.refresh_dropdown.pack(pady=2)

        # CPU
        ttk.Label(self.root, text="CPU Usage").pack()
        self.cpu_bar = ttk.Progressbar(self.root, length=350, style="Green.Horizontal.TProgressbar", maximum=100)
        self.cpu_bar.pack(pady=5)
        self.cpu_label = ttk.Label(self.root, text="0%", font=("Segoe UI", 10))
        self.cpu_label.pack()
        self.cpu_freq_label = ttk.Label(self.root, text="Frequency: 0 MHz", font=("Segoe UI", 10))
        self.cpu_freq_label.pack()
        # CPU Graph
        self.cpu_canvas = tk.Canvas(self.root, width=350, height=60, bg="#222")
        self.cpu_canvas.pack(pady=2)
        self.cpu_history = [0]*70

        # RAM
        ttk.Label(self.root, text="RAM Usage").pack()
        self.ram_bar = ttk.Progressbar(self.root, length=350, style="Green.Horizontal.TProgressbar", maximum=100)
        self.ram_bar.pack(pady=5)
        self.ram_label = ttk.Label(self.root, text="0%", font=("Segoe UI", 10))
        self.ram_label.pack()
        self.ram_detail_label = ttk.Label(self.root, text="Used: 0 GB / Total: 0 GB", font=("Segoe UI", 10))
        self.ram_detail_label.pack()
        # RAM Graph
        self.ram_canvas = tk.Canvas(self.root, width=350, height=60, bg="#222")
        self.ram_canvas.pack(pady=2)
        self.ram_history = [0]*70

        # Disk selection
        ttk.Label(self.root, text="Disk Usage").pack()
        self.disk_partitions = [p.device for p in psutil.disk_partitions() if os.path.exists(p.device)]
        self.selected_disk = tk.StringVar(value=self.disk_partitions[0] if self.disk_partitions else "/")
        self.disk_dropdown = ttk.Combobox(self.root, values=self.disk_partitions, textvariable=self.selected_disk, state="readonly", width=40)
        self.disk_dropdown.pack(pady=2)
        self.disk_bar = ttk.Progressbar(self.root, length=350, style="Green.Horizontal.TProgressbar", maximum=100)
        self.disk_bar.pack(pady=5)
        self.disk_label = ttk.Label(self.root, text="0%", font=("Segoe UI", 10))
        self.disk_label.pack()
        self.disk_detail_label = ttk.Label(self.root, text="Used: 0 GB / Total: 0 GB", font=("Segoe UI", 10))
        self.disk_detail_label.pack()
        self.disk_dropdown.bind("<<ComboboxSelected>>", self.on_disk_change)

        # Battery
        ttk.Label(self.root, text="Battery").pack()
        self.battery_label = ttk.Label(self.root, text="Checking...", font=("Segoe UI", 10))
        self.battery_label.pack(pady=5)

        # Network
        ttk.Label(self.root, text="Network Speed").pack()
        self.network_label = ttk.Label(self.root, text="Upload: 0 KB/s | Download: 0 KB/s", font=("Segoe UI", 10))
        self.network_label.pack(pady=5)

        # Uptime
        ttk.Label(self.root, text="System Uptime").pack()
        self.uptime_label = ttk.Label(self.root, text="0:00:00", font=("Segoe UI", 10))
        self.uptime_label.pack(pady=5)

        # Start monitoring thread
        threading.Thread(target=self.update_stats, daemon=True).start()

    def log_error(self, msg):
        with open("system_monitor_errors.log", "a") as f:
            f.write(f"{datetime.datetime.now()}: {msg}\n")

    def on_disk_change(self, event):
        pass

    def set_bar_color(self, bar, percent):
        if percent < 50:
            bar.config(style="Green.Horizontal.TProgressbar")
        elif percent < 80:
            bar.config(style="Yellow.Horizontal.TProgressbar")
        else:
            bar.config(style="Red.Horizontal.TProgressbar")

    def show_alert(self, resource, percent):
        messagebox.showwarning("High Usage Alert", f"{resource} usage is very high: {percent}%")

    def draw_graph(self, canvas, history, color):
        canvas.delete("all")
        h = int(canvas["height"])
        w = int(canvas["width"])
        points = []
        for i, val in enumerate(history):
            x = i * (w / len(history))
            y = h - (val / 100) * h
            points.append((x, y))
        for i in range(1, len(points)):
            canvas.create_line(points[i-1][0], points[i-1][1], points[i][0], points[i][1], fill=color, width=2)

    def update_stats(self):
        try:
            prev_sent = psutil.net_io_counters().bytes_sent
            prev_recv = psutil.net_io_counters().bytes_recv
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        except Exception as e:
            self.log_error(f"Init error: {e}")
            prev_sent = prev_recv = 0
            boot_time = datetime.datetime.now()

        while True:
            interval = self.refresh_rate.get()
            # CPU
            try:
                cpu = psutil.cpu_percent(interval=None)
                self.cpu_bar["value"] = cpu
                self.cpu_label.config(text=f"{cpu}%")
                self.set_bar_color(self.cpu_bar, cpu)
                freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
                self.cpu_freq_label.config(text=f"Frequency: {freq:.0f} MHz")
                self.cpu_history.append(cpu)
                self.cpu_history = self.cpu_history[-70:]
                self.draw_graph(self.cpu_canvas, self.cpu_history, "#4CAF50")
                if cpu > 90:
                    self.show_alert("CPU", cpu)
            except Exception as e:
                self.cpu_label.config(text="Error")
                self.cpu_bar["value"] = 0
                self.log_error(f"CPU error: {e}")

            # RAM
            try:
                ram = psutil.virtual_memory()
                ram_percent = ram.percent
                self.ram_bar["value"] = ram_percent
                self.ram_label.config(text=f"{ram_percent}%")
                self.set_bar_color(self.ram_bar, ram_percent)
                used_gb = ram.used / (1024**3)
                total_gb = ram.total / (1024**3)
                self.ram_detail_label.config(text=f"Used: {used_gb:.2f} GB / Total: {total_gb:.2f} GB")
                self.ram_history.append(ram_percent)
                self.ram_history = self.ram_history[-70:]
                self.draw_graph(self.ram_canvas, self.ram_history, "#FFC107")
                if ram_percent > 90:
                    self.show_alert("RAM", ram_percent)
            except Exception as e:
                self.ram_label.config(text="Error")
                self.ram_bar["value"] = 0
                self.log_error(f"RAM error: {e}")

            # Disk
            try:
                disk_device = self.selected_disk.get()
                disk = psutil.disk_usage(disk_device)
                disk_percent = disk.percent
                self.disk_bar["value"] = disk_percent
                self.disk_label.config(text=f"{disk_percent}%")
                self.set_bar_color(self.disk_bar, disk_percent)
                used_gb = disk.used / (1024**3)
                total_gb = disk.total / (1024**3)
                self.disk_detail_label.config(text=f"Used: {used_gb:.2f} GB / Total: {total_gb:.2f} GB")
                if disk_percent > 90:
                    self.show_alert("Disk", disk_percent)
            except Exception as e:
                self.disk_label.config(text="Error")
                self.disk_bar["value"] = 0
                self.disk_detail_label.config(text="Used: - GB / Total: - GB")
                self.log_error(f"Disk error: {e}")

            # Battery
            try:
                battery_info = psutil.sensors_battery()
                if battery_info:
                    battery = battery_info.percent
                    plugged = battery_info.power_plugged
                    self.battery_label.config(
                        text=f"{battery}% {'(Charging)' if plugged else '(Not Charging)'}"
                    )
                else:
                    self.battery_label.config(text="Battery info not available")
            except Exception as e:
                self.battery_label.config(text="Battery error")
                self.log_error(f"Battery error: {e}")

            # Network Speed
            try:
                net = psutil.net_io_counters()
                sent = net.bytes_sent
                recv = net.bytes_recv
                upload_speed = (sent - prev_sent) / 1024 / interval
                download_speed = (recv - prev_recv) / 1024 / interval
                prev_sent, prev_recv = sent, recv
                self.network_label.config(
                    text=f"↑ {upload_speed:.1f} KB/s | ↓ {download_speed:.1f} KB/s"
                )
            except Exception as e:
                self.network_label.config(text="Network error")
                self.log_error(f"Network error: {e}")

            # Uptime
            try:
                uptime = datetime.datetime.now() - boot_time
                self.uptime_label.config(text=str(uptime).split(".")[0])
            except Exception as e:
                self.uptime_label.config(text="Uptime error")
                self.log_error(f"Uptime error: {e}")

            time.sleep(interval)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    SystemMonitor(root)
    root.mainloop()