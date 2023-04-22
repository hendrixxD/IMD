#!/usr/bin/env python3
""" Block-based detection with Discrete cosine transform"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.decomposition import PCA
from sklearn.cluster import SpectralClustering


def block_based_D_WITH_DCT(filename):
    # Define the block size
    block_size = 16

    # Read an image
    img = cv2.imread(filename)
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert to float32
    img = img.astype(np.float32)
    # Get the image dimensions
    height, width = img.shape

    # Initialize an empty list to store the features
    features = []

    # Loop over the image blocks
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Get the current block
            block = img[i:i+block_size, j:j+block_size]
            # Flatten the block into a vector
            block_vector = block.flatten()
            # Append the vector to the features list
            features.append(block_vector)

    # Convert the features list to a numpy array
    features = np.array(features)

    # Apply PCA to reduce the dimensionality of the features
    pca = PCA(n_components=64, random_state=0)
    features_pca = pca.fit_transform(features)

    # Apply spectral clustering to the features with k=2
    sc = SpectralClustering(n_clusters=2, affinity='cosine', random_state=0)
    labels = sc.fit_predict(features_pca)

    # Initialize an empty image to store the forged regions
    forged_img = np.zeros_like(img)

    # Loop over the image blocks again
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Get the index of the current block in the features array
            index = (i // block_size) * (width // block_size) + (j // block_size)
            # Get the label of the current block
            label = labels[index]
            # If the label is 1, mark the block as forged on the forged image
            if label == 1:
                forged_img[i:i+block_size, j:j+block_size] = 255

    # Display the original and forged images
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(forged_img, cmap='jet')
    plt.title('Forged Regions')
    plt.axis('off')
    plt.show()
