import numpy as np
import matplotlib.pyplot as plt
import rasterio
import spectral
import os

# import matplotlib
# matplotlib.use('TkAgg')

def create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

header_file = 'P:/2023/Trial 33/Trial 33A/Trial 33A HeadwallDemoVNIR S3/20230802/ref/whiteref_l1.hdr'
data_file = 'P:/2023/Trial 33/Trial 33A/Trial 33A HeadwallDemoVNIR S3/20230802/ref/whiteref_l1.pcf'

with rasterio.open(data_file) as src:
    # Read the data
    hyperspectral_data = src.read()

# Accessing information from the header
samples = src.width
lines = src.height
bands = src.count
selected_band = 229  # Change this to the desired band number
# Extract the hyperspectral data

# Calculate the mean spectrum
mean_spectrum = np.mean(hyperspectral_data, axis=(0, 1))  # Assuming 3D data (height, width, bands)
# Extract the spatial profile for the selected band
mean_spatial_profile = np.mean(hyperspectral_data, axis=2)
spatial_profile = hyperspectral_data[:, :, selected_band]

save_folder = 'C:/Users/nmovahedi/Desktop/Result of VNIR cameras/HW-VNIR'

# Call the function to create the folder
create_folder(save_folder)

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(mean_spectrum, color='blue')
plt.title('Mean Spectrum of White Reference')
plt.xlabel('Band Number')
plt.ylabel('Mean Intensity')
plt.grid()

# Save the plot as an image in the specified folder
plt.savefig(f'{save_folder}/mean_spectrum of white reference.png')
plt.show()  # Show the mean spectrum plot

# Create a spatial profile plot
plt.figure(figsize=(10, 6))
plt.plot(mean_spatial_profile.T, color='blue')
plt.title(f'Spatial Profile - Band {selected_band}')
plt.xlabel('Pixel Index')
plt.ylabel('Intensity')
plt.grid()

# Save the plot as an image in the specified folder
plt.savefig(f'{save_folder}/mean_spatial_profile_of_White_Reference.png')
plt.show()  # Show the spatial profile plot
