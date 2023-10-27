import numpy as np
import scipy.io

# Load the hyperspectral image from the .mat file
mat_file = scipy.io.loadmat('N:/Post incubation trials/G9 Result/G9 Day 4/G9 Group A-Day 4/HSI/00001.mat')

# Extract the hyperspectral data
hyperspectral_image = mat_file['EGG']  # Replace 'your_variable_name' with the actual variable name in your .mat file

# Calculate the mean and standard deviation of the entire image
image_mean = np.mean(hyperspectral_image)
image_std = np.std(hyperspectral_image)

# Calculate SNR using the entire image statistics
snr = 10 * np.log10(image_mean ** 2 / image_std ** 2)

print(f"Signal-to-Noise Ratio (SNR): {snr} dB")
