from framework.energymonitor import EnergyMonitor

class LinuxEnergyMonitor(EnergyMonitor):
    def read_energy(self):
        try:
            with open('/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj', 'r') as f:
                energy = int(f.read().strip())
            return energy
        except FileNotFoundError:
            print("RAPL energy file not found. Ensure your system supports Intel RAPL.")
            exit(1)

    def get_total_cpu_time(self):
        with open('/proc/stat', 'r') as f:
            fields = f.readline().strip().split()
            total_time = sum(int(field) for field in fields[1:])
        return total_time

    def get_process_cpu_time(self, pid):
        with open(f'/proc/{pid}/stat', 'r') as f:
            fields = f.read().strip().split()
            utime = int(fields[13])  # User mode time
            stime = int(fields[14])  # Kernel mode time
            return utime + stime

if __name__ == "__main__":
    pid = input("Enter the PID to monitor: ")
    interval = float(input("Enter the measurement interval in seconds (default is 1.0): ") or "1.0")
    duration = float(input("Enter the total duration of measurement in seconds (default is 10): ") or "10")
    
    monitor = LinuxEnergyMonitor()
    monitor.measure_power_for_pid(pid, interval, duration)
