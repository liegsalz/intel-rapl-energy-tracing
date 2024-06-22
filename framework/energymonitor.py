from abc import ABC, abstractmethod
import time
import csv
from datetime import datetime

class EnergyMonitor(ABC):
    @abstractmethod
    def read_energy(self):
        """Read the current energy consumption in joules."""
        pass

    @abstractmethod
    def get_total_cpu_time(self):
        """Get the total CPU time."""
        pass

    @abstractmethod
    def get_process_cpu_time(self, pid):
        """Get the CPU time used by a specific process."""
        pass

    def measure_power_for_pid(self, pid, interval=1.0, duration=10.0):
        """Measure the power consumption for a specific PID."""
        start_energy = self.read_energy()
        start_total_cpu_time = self.get_total_cpu_time()
        start_process_cpu_time = self.get_process_cpu_time(pid)

        total_energy_consumed = 0
        accum_data = []
        consumption_data = []

        for _ in range(int(duration / interval)):
            time.sleep(interval)

            current_energy = self.read_energy()
            current_total_cpu_time = self.get_total_cpu_time()
            current_process_cpu_time = self.get_process_cpu_time(pid)

            system_energy_diff = (current_energy - start_energy) / 1e6  # Convert µJ to J
            total_cpu_time_diff = current_total_cpu_time - start_total_cpu_time
            process_cpu_time_diff = current_process_cpu_time - start_process_cpu_time

            if total_cpu_time_diff > 0:
                process_energy = system_energy_diff * (process_cpu_time_diff / total_cpu_time_diff)
            else:
                process_energy = 0

            total_energy_consumed += process_energy
            power = process_energy / interval
            print(f"Power consumption for PID {pid}: {power:.3f} W")

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            accum_data.append([timestamp, total_energy_consumed])
            consumption_data.append([timestamp, process_energy / 3_600_000])  # Convert J to kWh

            start_energy = current_energy
            start_total_cpu_time = current_total_cpu_time
            start_process_cpu_time = current_process_cpu_time

        total_energy_kwh = total_energy_consumed / 3_600_000
        print(f"Total energy consumption for PID {pid} over {duration} seconds: {total_energy_kwh:.6f} kWh")

        self.write_power_data_to_file(accum_data, consumption_data, "accum_data.csv", "consumption_data.csv")

    def write_power_data_to_file(self, accum_data, consumption_data, accum_filename, consumption_filename):
        """Write power data to files.
        
        args:
        accum_data: list of lists, where each list contains a timestamp and accumulated power consumption in Joules
        consumption_data: list of lists, where each list contains a timestamp and power consumption in kWh
        accum_filename: name of the file to write the accumulated power data
        consumption_filename: name of the file to write the power consumption data
        """
        with open(accum_filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Timestamp', 'Accumulated Power Consumption (Watts)'])
            writer.writerows(accum_data)

        with open(consumption_filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Timestamp', 'Power Consumption (kWh)'])
            writer.writerows(consumption_data)