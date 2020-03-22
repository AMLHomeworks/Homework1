import numpy as np
import math



# Compute the intersection distance between histograms x and y
# Return 1 - hist_intersection, so smaller values correspond to more similar histograms
# Check that the distance range in [0,1]

def dist_intersect(x,y, normalized=False):
    
    #... (your code here)
    if type(x) != np.ndarray:
        x = np.array(x)
    if type(y) != np.ndarray:
        y = np.array(y)
    
    sum_ = np.sum(np.minimum(x,y))

    if not normalized:
        return 1 - 0.5*(sum_/np.sum(x) + sum_/np.sum(y))
    else:
        return 1 - sum_



# Compute the L2 distance between x and y histograms
# Check that the distance range in [0,sqrt(2)]

def dist_l2(x,y):
    
    #... (your code here)
    if type(x) != np.ndarray:
        x = np.array(x)
    if type(y) != np.ndarray:
        y = np.array(y)
    
    distance = np.sum([(a-b)**2 for a, b in zip(x, y)])

    assert distance > 0, "Distance must be in the range [0,sqrt(2)]"

    return distance



# Compute chi2 distance between x and y
# Check that the distance range in [0,Inf]
# Add a minimum score to each cell of the histograms (e.g. 1) to avoid division by 0

def dist_chi2(x,y):
    
    #... (your code here)
    if type(x) != np.ndarray:
        x = np.array(x)
    if type(y) != np.ndarray:
        y = np.array(y)
    # Add a minimum score to each cell of the histograms (e.g. 1) to avoid division by 0
    x = (x==0) * 0.0001 + x
    y = (y==0) * 0.0001 + y
    
    chi2 = np.sum([((a-b)**2)/(a+b) for a, b in zip(x, y)])

    assert chi2 > 0, "chi square score must be in the range [0,Inf]"
    
    return chi2


def get_dist_by_name(x, y, dist_name):
  if dist_name == 'chi2':
    return dist_chi2(x,y)
  elif dist_name == 'intersect':
    return dist_intersect(x,y)
  elif dist_name == 'l2':
    return dist_l2(x,y)
  else:
    assert False, 'unknown distance: %s'%dist_name
  




