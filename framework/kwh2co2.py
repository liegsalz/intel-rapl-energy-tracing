def calculate_co2_emissions(energy_kwh, carbon_intensity=354):
    co2_emissions = energy_kwh * carbon_intensity
    return co2_emissions
