import numpy as np
from numpy import histogram as hist



#Add the Filtering folder, to import the gauss_module.py file, where gaussderiv is defined (needed for dxdy_hist)
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
filteringpath = os.path.join(parentdir, 'Filtering')
sys.path.insert(0,filteringpath)
import gauss_module



#  compute histogram of image intensities, histogram should be normalized so that sum of all values equals 1
#  assume that image intensity varies between 0 and 255
#
#  img_gray - input image in grayscale format
#  num_bins - number of bins in the histogram
def normalized_hist(img_gray, num_bins, _range = (0,255)):
    assert len(img_gray.shape) == 2, 'image dimension mismatch'
    assert img_gray.dtype == 'float', 'incorrect image type'

    arr = img_gray.ravel()

    def rounder(values):
        def f(x):
            idx = np.argmin(np.abs(values - x))
            return values[idx]
        return np.frompyfunc(f, 1, 1)

    bins = np.array([i * _range[1]/num_bins for i in range(num_bins+1)])
    arr = np.array([rounder(bins)(i) for i in arr])
    arr = np.bincount((arr*num_bins/_range[1]).astype(int))
    hists = np.zeros(num_bins)

    if len(arr) <= num_bins:
        hists[:len(arr)] = arr
    else:
        hists = arr[:num_bins]

    # normalize
    hists = hists/np.sum(hists)

    return hists, bins



#  Compute the *joint* histogram for each color channel in the image
#  The histogram should be normalized so that sum of all values equals 1
#  Assume that values in each channel vary between 0 and 255
#
#  img_color - input color image
#  num_bins - number of bins used to discretize each channel, total number of bins in the histogram should be num_bins^3
#
#  E.g. hists[0,9,5] contains the number of image_color pixels such that:
#       - their R values fall in bin 0
#       - their G values fall in bin 9
#       - their B values fall in bin 5
def rgb_hist(img_color_double, num_bins):
    assert len(img_color_double.shape) == 3, 'image dimension mismatch'
    assert img_color_double.dtype == 'float', 'incorrect image type'

    bin_size = 256/num_bins
    #Define a 3D histogram  with "num_bins^3" number of entries
    hists = np.zeros((num_bins, num_bins, num_bins))

    
    red = img_color_double[:,:,0].ravel()
    green = img_color_double[:,:,1].ravel()
    blue = img_color_double[:,:,2].ravel()

    # Loop for each pixel i in the image 
    for i in range(img_color_double.shape[0]*img_color_double.shape[1]):
        # Increment the histogram bin which corresponds to the R,G,B value of the pixel i
        r = int(np.floor(red[i]/bin_size)) + 1
        g = int(np.floor(green[i]/bin_size)) + 1
        b = int(np.floor(blue[i]/bin_size)) + 1
        hists[r-1,g-1,b-1] = hists[r-1,g-1,b-1] + 1

    #Return the histogram as a 1D vector
    hists = hists.reshape(hists.size)

    #Normalize the histogram such that its integral (sum) is equal 1
    #... (your code here)
    hists = hists/np.sum(hists)

    return hists



#  Compute the *joint* histogram for the R and G color channels in the image
#  The histogram should be normalized so that sum of all values equals 1
#  Assume that values in each channel vary between 0 and 255
#
#  img_color - input color image
#  num_bins - number of bins used to discretize each channel, total number of bins in the histogram should be num_bins^2
#
#  E.g. hists[0,9] contains the number of image_color pixels such that:
#       - their R values fall in bin 0
#       - their G values fall in bin 9
def rg_hist(img_color_double, num_bins):
    assert len(img_color_double.shape) == 3, 'image dimension mismatch'
    assert img_color_double.dtype == 'float', 'incorrect image type'


    bin_size = 256/num_bins
    #Define a 2D histogram  with "num_bins^2" number of entries
    hists = np.zeros((num_bins, num_bins))

    red = img_color_double[:,:,0].ravel()
    green = img_color_double[:,:,1].ravel()

    # Loop for each pixel i in the image
    for i in range(img_color_double.shape[0]*img_color_double.shape[1]):
        # Increment the histogram bin which corresponds to the R,G,B value of the pixel i
        r = int(np.floor(red[i]/bin_size)) + 1
        g = int(np.floor(green[i]/bin_size)) + 1
        hists[r-1,g-1] = hists[r-1,g-1] + 1

    #Return the histogram as a 1D vector
    hists = hists.reshape(hists.size)

    #Normalize
    hists = hists/np.sum(hists)

    return hists




#  Compute the *joint* histogram of Gaussian partial derivatives of the image in x and y direction
#  Set sigma to 3.0 and cap the range of derivative values is in the range [-6, 6]
#  The histogram should be normalized so that sum of all values equals 1
#
#  img_gray - input gray value image
#  num_bins - number of bins used to discretize each dimension, total number of bins in the histogram should be num_bins^2
#
#  Note: you may use the function gaussderiv from the Filtering exercise (gauss_module.py)
def dxdy_hist(img_gray, num_bins):
    assert len(img_gray.shape) == 2, 'image dimension mismatch'
    assert img_gray.dtype == 'float', 'incorrect image type'

    bin_size = 256/num_bins
    #Define a 2D histogram  with "num_bins^2" number of entries
    hists = np.zeros((num_bins, num_bins))

    [imgDx, imgDy] = gauss_module.gaussderiv(img_gray, 3.0)

    imgDx = 12*(imgDx-np.min(imgDx))/(np.max(imgDx)-np.min(imgDx)) - 6
    imgDy = 12*(imgDy-np.min(imgDy))/(np.max(imgDy)-np.min(imgDy)) - 6

    imgDx = imgDx.ravel()
    imgDy = imgDy.ravel()
    
    for i in range(img_gray.shape[0]*img_gray.shape[1]):
        x = int(np.floor(imgDx[i]/bin_size)) + 1
        y = int(np.floor(imgDy[i]/bin_size)) + 1
        hists[x-1,y-1] = hists[x-1,y-1] + 1

    #Return the histogram as a 1D vector
    hists = hists.reshape(hists.size)
    return hists



def is_grayvalue_hist(hist_name):
  if hist_name == 'grayvalue' or hist_name == 'dxdy':
    return True
  elif hist_name == 'rgb' or hist_name == 'rg':
    return False
  else:
    assert False, 'unknown histogram type'


def get_hist_by_name(img, num_bins_gray, hist_name):
  if hist_name == 'grayvalue':
    return normalized_hist(img, num_bins_gray)
  elif hist_name == 'rgb':
    return rgb_hist(img, num_bins_gray)
  elif hist_name == 'rg':
    return rg_hist(img, num_bins_gray)
  elif hist_name == 'dxdy':
    return dxdy_hist(img, num_bins_gray)
  else:
    assert False, 'unknown distance: %s'%hist_name

