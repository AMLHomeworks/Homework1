import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import histogram_module
import dist_module

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray



# model_images - list of file names of model images
# query_images - list of file names of query images
#
# dist_type - string which specifies distance type:  'chi2', 'l2', 'intersect'
# hist_type - string which specifies histogram type:  'grayvalue', 'dxdy', 'rgb', 'rg'
#
# note: use functions 'get_dist_by_name', 'get_hist_by_name' and 'is_grayvalue_hist' to obtain 
#       handles to distance and histogram functions, and to find out whether histogram function 
#       expects grayvalue or color image

def find_best_match(model_images, query_images, dist_type, hist_type, num_bins):

    hist_isgray = histogram_module.is_grayvalue_hist(hist_type)
    
    model_hists = compute_histograms(model_images, hist_type, hist_isgray, num_bins)
    query_hists = compute_histograms(query_images, hist_type, hist_isgray, num_bins)
    
    D = np.zeros((len(query_images), len(model_images)))
    best_match = np.zeros((len(query_images), len(model_images)))

    for i in range(len(query_images)):
        for j in range(len(model_images)):
            D[i, j] = dist_module.get_dist_by_name(query_hists[i], model_hists[j], dist_type)

        best_match[i] = np.argsort(D[i])
    #... (your code here)
    best_match = best_match[:,0]
    best_match = best_match.astype(int)

    return best_match, D



def compute_histograms(image_list, hist_type, hist_isgray, num_bins):
    
    image_hist = []

    # Compute hisgoram for each image and add it at the bottom of image_hist

    #... (your code here)
    for img in image_list:
        img_color = np.array(Image.open(img))

        if hist_isgray:
            img_color = rgb2gray(img_color.astype('double'))           
        hist = histogram_module.get_hist_by_name(img_color.astype('double'), num_bins, hist_type)

        if len(hist) == 2:
            hist = hist[0]

        image_hist.append(hist)
    
    return image_hist



# For each image file from 'query_images' find and visualize the 5 nearest images from 'model_image'.
#
# Note: use the previously implemented function 'find_best_match'
# Note: use subplot command to show all the images in the same Python figure, one row per query image

def show_neighbors(model_images, query_images, dist_type, hist_type, num_bins):
    
    plt.figure()

    num_nearest = 5  # show the top-5 neighbors

    [best_match, D] = find_best_match(model_images, query_images, dist_type, hist_type, num_bins)

    D = np.around(D,3)
    matches = np.zeros((len(query_images), num_nearest))
    for i in range(len(query_images)):
        matches[i] = np.argsort(D[i])[:num_nearest]
    matches = matches.astype(int)

    for i in range(len(query_images)):
        plt.subplot(i+1,6,1); plt.imshow(np.array(Image.open(query_images[i])), vmin=0, vmax=255)
        plt.title(f'Q{i}')
        plt.subplot(i+1,6,2); plt.imshow(np.array(Image.open(model_images[matches[i][0]])), vmin=0, vmax=255)
        plt.title(f'M{D[i][matches[i][0]]}')
        plt.subplot(i+1,6,3); plt.imshow(np.array(Image.open(model_images[matches[i][1]])), vmin=0, vmax=255)
        plt.title(f'M{D[i][matches[i][1]]}')
        plt.subplot(i+1,6,4); plt.imshow(np.array(Image.open(model_images[matches[i][2]])), vmin=0, vmax=255)
        plt.title(f'M{D[i][matches[i][2]]}')
        plt.subplot(i+1,6,5); plt.imshow(np.array(Image.open(model_images[matches[i][3]])), vmin=0, vmax=255)
        plt.title(f'M{D[i][matches[i][3]]}')
        plt.subplot(i+1,6,6); plt.imshow(np.array(Image.open(model_images[matches[i][4]])), vmin=0, vmax=255)
        plt.title(f'M{D[i][matches[i][4]]}')
        plt.show()
