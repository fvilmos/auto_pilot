# fvilmos, https://github.com/fvilmos
import numpy as np

class ConvertDirection(object):
    
    def __init__(self):
        pass

    
    def __call__(self,item):
        
        #operates directly on data
        direction = np.array(item[2])
        
        fdir = 0
        if direction == 'forward':
            fdir = 1
        elif direction == 'left':
            fdir = 0
        elif direction == 'right':
            fdir = 2
        elif direction == 'keep_lane':
            fdir = 1
            
        return item[0],item[1],fdir
