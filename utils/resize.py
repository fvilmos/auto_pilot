# fvilmos, https://github.com/fvilmos

import cv2
import numpy as np

class Resize(object):
    
    def __init__(self,new_size=None):
        self.new_size = new_size
    
    def __call__(self,item):
        img = item[0]
        img = cv2.resize(img, self.new_size, interpolation = cv2.INTER_AREA)

        ret = np.array(img)
        
        return ret,item[1],item[2]