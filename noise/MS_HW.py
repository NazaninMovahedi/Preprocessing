import numpy as np
import matplotlib.pyplot as plt
import spectral
import os
from scipy.ndimage import uniform_filter
import matplotlib
matplotlib.use('TkAgg')

def create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

header_file = 'P:/2023/Trial 33/Trial 33A/Trial 33A HeadwallDemoVNIR S3/20230802/ref/dark current 1/egg_3_2023-08-02_11-43-36.hdr'
data_file = 'P:/2023/Trial 33/Trial 33A/Trial 33A HeadwallDemoVNIR S3/20230802/ref/dark current 1/egg_3_2023-08-02_11-43-36.pcf'

# Load the ENVI header and data by specifying the data file
data = spectral.envi.open(header_file, data_file)

# Accessing information from the header
header = data.metadata
bands = int(header['bands'])

# Specify the start and end bands
start_band = 0  # Adjust this value based on your start band of interest
end_band = 300   # Adjust this value based on your end band of interest

# Ensure the specified bands are within the available range
start_band = max(start_band, 0)
end_band = min(end_band, bands - 1)

# Extract the hyperspectral data for the specified range of bands
hyperspectral_data = data.load()[:, :, start_band:end_band + 1]

# Calculate the mean spectrum (across all pixels)
mean_spectrum = np.mean(hyperspectral_data, axis=(0, 1))
window_size = 70  # Adjust the window size as needed for smoother results

mean_spectrum_baseline = uniform_filter(mean_spectrum, size=window_size)

# Calculate the spatial mean (across all bands)
spatial_mean = np.mean(hyperspectral_data, axis=2)

# Create a plot for the mean spectrum
plt.figure(figsize=(10, 6))
plt.plot(mean_spectrum, color='blue', label='Mean Spectrum')
plt.plot(mean_spectrum_baseline, color='red', label='Smoothed Baseline')
plt.title(f'Mean Spectrum of Tray reference - Bands {start_band} to {end_band}')
plt.xlabel('Band Number')
plt.ylabel('Mean Intensity')
plt.grid()
plt.legend()

# Save the plot as an image in the specified folder
save_folder = 'C:/Users/nmovahedi/Desktop/Result of VNIR cameras/HW-VNIR'
create_folder(save_folder)
plt.savefig(f'{save_folder}/mean_spectrum_Tray_reference_{start_band}_to_{end_band}.png')
plt.show()  # Show the mean spectrum plot

# Create a plot for the spatial mean
plt.figure(figsize=(10, 6))
plt.plot(spatial_mean.T, color='blue', label='Original Spatial Mean')

# Smooth the spatial mean for visualization
smoothed_spatial_mean = uniform_filter(spatial_mean, size=window_size)

plt.plot(smoothed_spatial_mean.T, color='red', label='Smoothed Spatial Mean')
plt.title('Spatial Mean across Bands of Tray reference')
plt.xlabel('Pixel Index')
plt.ylabel('Mean Intensity')
plt.grid()
plt.legend()

# Save the plot as an image in the specified folder
plt.savefig(f'{save_folder}/spatial_mean_across_bands_Tray_reference.png')
plt.show()  # Show the spatial mean plot
