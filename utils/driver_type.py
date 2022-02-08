# fvilmos, https://github.com/fvilmos
class DriverType:
    def __init__(self):
        """
        Sets the desired state (data recording - with autopilot, manual, inference)
        """
        # autopilot = 0, manual = 1, inference = 2 ...
        self.dtype=0
        
    @property
    def get_driver_type(self):
        return self.dtype
    
    def set_driver_type(self,item):
        self.dtype = item
    
    @property        
    def autopilot(self):
        return 0

    @property
    def manual(self):
        return 1
                    
    @property        
    def inference(self):
        return 2
    
    @property        
    def crazyautopilot(self):
        return 3
    
    def __eq__(self, item):
        return self.dtype == item
        