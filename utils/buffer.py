# fvilmos, https://github.com/fvilmos
import numpy as np

class Buffer():
    """
    Used to creat an array of N consecutive images
    """
    def __init__(self, shape=[60,320,3], buff_length=3):
        self.skip_counter = 0
        arr = np.zeros(shape)
        self.ibuffer = [arr for i in range(buff_length)]
        
    def update(self,val,skipp_rate=0):
        
        # delete the oldest, put a new mg in the buffer
        if self.skip_counter == skipp_rate:
            self.ibuffer.pop(0)
            self.ibuffer.append(val)
            self.skip_counter = 0
        else:
            self.skip_counter +=1

        return np.array(self.ibuffer)
    
    def get_buffer(self):
        return np.array(self.ibuffer)