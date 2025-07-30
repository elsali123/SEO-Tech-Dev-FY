import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import os

# Load and compress image progressively using SVD

def load_image(image_path):
    """Load image and return as a NumPy array."""
    return img.imread(image_path)

def compress_channel(channel, k):
    """Compress a single channel using SVD with k singular values."""
    U, s, Vt = np.linalg.svd(channel, full_matrices=False)  # Break into matrices
    S = np.diag(s[:k])  # Keep top k values from the diagonal
    return U[:, :k] @ S @ Vt[:k, :]  # Reconstruct using reduced info

def compress_image_color(img, k):
    """Compress all 3 color channels (R, G, B) using SVD with k values each. """
    r = compress_channel(img[:, :, 0], k)
    g = compress_channel(img[:, :, 1], k)
    b = compress_channel(img[:, :, 2], k)

    # Combine the 3 channels into one image, making sure values stay in range [0, 1]
    compressed_img = np.stack([r, g, b], axis=2)
    compressed_img = np.clip(compressed_img, 0, 1)
    return compressed_img


def save_compressed_image(image, output_path):
    """Save compressed image"""
    plt.imsave(output_path, image)

def generate_compression_stages(image_path, stages, output_dir):
    """ Generate and save a sequence of progressively less compressed images. """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    original_img = load_image(image_path)

    image_number = 1
    for k in stages:
        compressed_img = compress_image_color(original_img, k)

        filename = "compressed_stage_" + str(image_number) + ".png"
        save_path = os.path.join(output_dir, filename)

        save_compressed_image(compressed_img, save_path)
        print("Saved", filename, "with k =", k)

        image_number += 1


# Implementation
if __name__ == '__main__':
    image_path = 'assets/background/rainforest.png'  # Replace with your image file
    compression_stages = [15, 35, 50, 100]  # Adjust as needed
    output_folder = 'assets/compressed_backgrounds'

    generate_compression_stages(image_path, compression_stages, output_folder)
