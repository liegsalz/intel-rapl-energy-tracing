import matplotlib.pyplot as plt
import pandas as pd

from poc.framework.kwh2co2 import calculate_co2_emissions

def plot_consumption_from_csv(file_path1):
    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(file_path1, sep=',', parse_dates=['Timestamp'])
    accum_path1 = file_path1.replace('.csv', '_accum.csv')
    df1_accum = pd.read_csv(accum_path1, sep=',', parse_dates=['Timestamp'])

    # Normalize the timestamps by setting the first value to zero
    df1['DeltaTime'] = (df1['Timestamp'] - df1['Timestamp'].iloc[0]).dt.total_seconds()
    df1_accum['DeltaTime'] = (df1_accum['Timestamp'] - df1_accum['Timestamp'].iloc[0]).dt.total_seconds()
    
    # Calculate CO2 emissions based on Power Consumption (kWh)
    df1['Power Consumption (kW)'] = df1['Power Consumption (Watts)'].apply(lambda consumption: consumption / 1000)
    
    df1_accum['Accumulated CO2 Emissions (grams)'] = df1_accum['Accumulated Power Consumption (kWh)'].apply(calculate_co2_emissions)
    
    # Create subplots side by side
    _, (ax1) = plt.subplots(1, 1, figsize=(15, 15))
    
    # Plot Power Consumption
    ax1.plot(df1['DeltaTime'], df1['Power Consumption (kW)'], marker='.', linestyle=':', color='b', label='Fibonacci Series')
    ax1.set_xlabel('Time (seconds from start)')
    ax1.set_ylabel('Power Consumption (kW)')
    ax1.set_title('Power Consumption Over Time')
    ax1.grid(True)
    ax1.legend()
    ax1.set_ylim(0)
    ax1.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
    
# Example usage
plot_consumption_from_csv('pow_cons_fib.csv', 'pow_cons_fib.csv')