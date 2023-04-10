import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import SpectralClustering

def detect_forgery_dct(image_path, block_size=16, n_components=64, n_clusters=2):
    # Read the image
    img = cv2.imread(image_path)
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert to float32
    img = img.astype(np.float32)
    # Get the image dimensions
    height, width = img.shape

    # Crop the image to a size that's a multiple of the block size
    height, width = height // block_size * block_size, width // block_size * block_size
    img = img[:height, :width]

    # Initialize an empty list to store the features
    features = []

    # Loop over the image blocks
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = img[i:i+block_size, j:j+block_size]
            block_vector = block.flatten()
            features.append(block_vector)

    # Convert the features list to a numpy array
    features = np.array(features)

    # Apply PCA to reduce the dimensionality of the features
    pca = PCA(n_components=n_components, random_state=0)
    features_pca = pca.fit_transform(features)

    # Apply spectral clustering to the features with k=n_clusters
    sc = SpectralClustering(n_clusters=n_clusters, affinity='cosine', random_state=0)
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

    # Return the forged image
    return forged_img

forged_img = detect_forgery_dct('./static/images/back_image-removebg.png')
print(forged_img)