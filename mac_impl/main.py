import subprocess
import psutil
import re

from framework.energymonitor import EnergyMonitor

class MacOSEnergyMonitor(EnergyMonitor):
    def read_energy(self):
        try:
            process = subprocess.Popen(
                ["sudo", "powermetrics", "--samplers", "cpu_power", "-i", "1", "-n", "1"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(timeout=10)
            if stderr:
                print("Error capturing powermetrics data:", stderr.decode())
                return None

            match = re.search(r"CPU Power:\s(\d+)", stdout.decode())
            if match:
                return float(match.group(1)) / 1000  # Convert mW to W
            else:
                print("Could not find CPU power data in powermetrics output.")
                return None

        except subprocess.TimeoutExpired:
            process.kill()
            print("Timeout expired for powermetrics command.")
            return None
        except Exception as e:
            print(f"Exception occurred: {e}")
            return None

    def get_total_cpu_time(self):
        return sum(psutil.cpu_times())

    def get_process_cpu_time(self, pid):
        process = psutil.Process(pid)
        cpu_times = process.cpu_times()
        return cpu_times.user + cpu_times.system

if __name__ == "__main__":
    pid = int(input("Enter the PID to monitor: "))
    interval = float(input("Enter the measurement interval in seconds (default is 0.1): ") or "0.1")
    duration = float(input("Enter the total duration of measurement in seconds (default is 10): ") or "10")

    monitor = MacOSEnergyMonitor()
    monitor.measure_power_for_pid(pid, interval, duration)
