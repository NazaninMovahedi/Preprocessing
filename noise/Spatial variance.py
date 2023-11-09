import cv2  # OpenCV for image processing (you may need to install it)

# Load your hyperspectral image here, replace 'image_data' with your data
# You should have a 3D NumPy array, where the third dimension represents spectral bands
# Example: image_data = np.load('your_hyperspectral_image.npy')

# Define the size of the local region (e.g., 5x5 pixel neighborhood)
region_size = 5

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

        # Update the spatial variance with the variance of the current band
        spatial_var += local_var / num_bands

    return spatial_var

# Calculate spatial variance
spatial_var = spatial_variance(image_data, region_size)
