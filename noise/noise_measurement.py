import numpy as np
import spectral
import matplotlib.pyplot as plt

# Define the path to the header and data files
header_file = 'data/raw.hdr'
data_file = 'data/raw'

# Load the ENVI header and data
header = spectral.envi.read_envi_header(header_file)
data = spectral.envi.open(header_file, data_file)

# Accessing information from the header
samples = header['samples']
lines = header['lines']
bands = header['bands']
interleave = header['interleave']
data_type = header['data type']

# Your code continues here...
print(samples)
# peak_band_index = np.argmax(np.max(data, axis=(0, 1)))

# Extract the peak band
peak_band = data[:, :, 103]

# Display the peak band using matplotlib
plt.imshow(peak_band, cmap='gray')
plt.title(f'Peak Band - Band {103 + 1}')
plt.colorbar()
plt.show()