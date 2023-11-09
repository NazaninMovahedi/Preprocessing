import numpy as np
import spectral
import matplotlib.pyplot as plt
import warnings
import cv2  # OpenCV for image processing (you may need to install it)
import matplotlib
matplotlib.use('TkAgg')
warnings.filterwarnings("ignore", category=RuntimeWarning)
# Define the path to the header and data files
header_file = 'P:/2023/Trial 25/Trial 25 S2/Calibration/Calibration  2.05/dark current 1/2023_03_03_10_03_20/raw.hdr'
data_file = 'P:/2023/Trial 25/Trial 25 S2/Calibration/Calibration  2.05/dark current 1/2023_03_03_10_03_20/raw'
region_size = 10
# Load the ENVI header and data
header = spectral.envi.read_envi_header(header_file)
data = spectral.envi.open(header_file, data_file)

# Accessing information from the header
samples = header['samples']
lines = header['lines']
bands = int(header['bands'])  # Convert 'bands' to an integer
interleave = header['interleave']
data_type = header['data type']

# Extract the hyperspectral data
hyperspectral_data = data.load()
peak_band = hyperspectral_data[:, :, 103]

std_deviation = np.std(hyperspectral_data, axis=2)

noise_mask = peak_band < 0.2
signal_mask = peak_band >= 0.5

reshaped_noise_mask = noise_mask[:, :, np.newaxis]

# Apply the masks to the hyperspectral data using element-wise multiplication
noise_regions = np.zeros_like(hyperspectral_data)
signal_regions = np.zeros_like(hyperspectral_data)

# Apply the masks to the hyperspectral data for each band
for band_idx in range(bands):
    noise_regions[:, :, band_idx] = hyperspectral_data[:, :, band_idx] * noise_mask
    signal_regions[:, :, band_idx] = hyperspectral_data[:, :, band_idx] * signal_mask

# Calculate statistics on the masked regions for each band
cv_values = np.std(noise_regions, axis=(0, 1)) / np.mean(noise_regions, axis=(0, 1))
snr_values = np.std(signal_regions, axis=(0, 1)) / np.std(noise_regions, axis=(0, 1))


# Print or further process the cv_values and snr_values for each band
for band_idx, (cv, snr) in enumerate(zip(cv_values, snr_values)):
    print(f"Band {band_idx + 1} - CV: {cv}, SNR: {snr}")

band_indices = list(range(1, bands + 1))

# Create bar plots to visualize CV and SNR for each band
plt.figure(figsize=(10, 8))

# Bar plot for CV
plt.subplot(3, 1, 1)
plt.bar(band_indices, cv_values, color='b', alpha=0.7)
plt.title('Coefficient of Variation (CV) for Each Band')
plt.xlabel('Band Index')
plt.ylabel('CV')

# Bar plot for SNR
plt.subplot(3, 1, 2)
plt.bar(band_indices, snr_values, color='g', alpha=0.7)
plt.title('Signal-to-Noise Ratio (SNR) for Each Band')
plt.xlabel('Band Index')
plt.ylabel('SNR')

# Create a bar chart to visualize the standard deviation
plt.subplot(3, 1, 3)
plt.bar(band_indices, std_deviation, color='g', alpha=0.7)
# plt.imshow(std_deviation, cmap='viridis')
plt.title('Standard Deviation of Hyperspectral Image')
plt.colorbar(label='Standard Deviation')
plt.show()

plt.tight_layout()
plt.show()


image = hyperspectral_data
# Calculate the spatial variance

def spatial_variance(image, region_size):
    # Calculate the number of bands
    num_bands = image.shape[2]

    # Initialize an array to store spatial variance for each pixel
    spatial_var = np.zeros_like(image[:, :, 0])

    # Iterate over each band
    for band in range(num_bands):
        # Apply a local variance calculation (filter2D) to each band
        band_data = image[:, :, band]
        local_var = cv2.filter2D(band_data, -1, np.ones((region_size, region_size)))
        local_var = local_var[:, :, np.newaxis]
        # Accumulate the local variances
        spatial_var += local_var

    # Average the accumulated variances
    spatial_var /= num_bands

    # Display spatial variance as an image
    plt.imshow(spatial_var, cmap='viridis')
    plt.title('Spatial Variance')
    plt.colorbar()
    plt.show()

# Calculate and display spatial variance
spatial_variance(hyperspectral_data, region_size)
