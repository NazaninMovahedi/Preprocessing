import numpy as np
import matplotlib.pyplot as plt
import spectral
from scipy.ndimage import uniform_filter

# import matplotlib
# matplotlib.use('TkAgg')
header_file = 'P:/2023/Trial 40/S2/ref/ref difusion sheet/et 28 fr 33/emptyname_2023-11-03_14-19-11/capture/emptyname_2023-11-03_14-19-11.hdr'
data_file = 'P:/2023/Trial 40/S2/ref/ref difusion sheet/et 28 fr 33/emptyname_2023-11-03_14-19-11/capture/emptyname_2023-11-03_14-19-11.raw'
save_folder = 'C:/Users/nmovahedi/Desktop/Result of VNIR cameras/Specim VNIR'

# Load the ENVI header and data
header = spectral.envi.read_envi_header(header_file)
data = spectral.envi.open(header_file, data_file)

# Accessing information from the header
samples = header['samples']
lines = header['lines']
bands = int(header['bands'])  # Convert 'bands' to an integer
interleave = header['interleave']
data_type = header['data type']
selected_band = 229  # Change this to the desired band number
window_size = 100
# Extract the hyperspectral data
hyperspectral_data = data.load()

# Calculate the mean spectrum
mean_spectrum = np.mean(hyperspectral_data, axis=(0, 1))  # Assuming 3D data (height, width, bands)

# Extract the spatial profile for the selected band
mean_spatial_profile = hyperspectral_data[:, :, selected_band].mean(axis=(0))

# Debugging prints
print("hyperspectral_data shape:", hyperspectral_data.shape)
print("mean_spatial_profile shape:", mean_spatial_profile.shape)
print("mean_spatial_profile values:", mean_spatial_profile)

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(mean_spectrum, color='blue')
smoothed_mean_spectrum = uniform_filter(mean_spectrum, size=window_size)
plt.plot(smoothed_mean_spectrum, color='red', label='Smoothed Spatial Mean')
plt.title('Mean Spectrum of White Reference')
plt.xlabel('Band Number')
plt.ylabel('Mean Intensity')
plt.grid()

# Save the plot as an image in the specified folder
plt.savefig(f'{save_folder}/mean_spectrum of White reference.png')
plt.show()  # Show the mean spectrum plot

# Create a spatial profile plot
plt.figure(figsize=(10, 6))
plt.plot(mean_spatial_profile, color='blue')
smoothed_spatial_mean = uniform_filter(mean_spatial_profile, size=window_size)
plt.plot(smoothed_spatial_mean, color='red', label='Smoothed Spatial Mean')
plt.title(f'Spatial Profile of White Reference - Band {selected_band}')
plt.xlabel('Pixel Index')
plt.ylabel('Intensity')
plt.grid()
plt.legend()
# Save the plot as an image in the specified folder
plt.savefig(f'{save_folder}/mean_spatial_profile_of_White_Reference.png')
plt.show()  # Show the spatial profile plot
