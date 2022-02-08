# fvilmos, https://github.com/fvilmos
import numpy as np

class AnomalyInjector():
    def __init__(self,auto_frame=50, man_frames=25) -> None:
        self.auto_frame = auto_frame
        self.man_frames = man_frames
        self.inits = [auto_frame,man_frames]
        self.vcontrol_tmp = None

    def run(self, vehicle, vcontrol):

        if self.auto_frame > 0:
            self.auto_frame -=1
            self.vcontrol_tmp = vcontrol
            vehicle.set_autopilot(True)
            vcontrol.throttle = 0.4
        else:
            if self.man_frames > 0:
                self.man_frames -=1
                vehicle.set_autopilot(False)
                vcontrol = self.vcontrol_tmp
                vcontrol.steer = np.random.choice([-0.7,-0.6,-0.5,-0.4,-0.2,0,0.2,0.4,0.5,0.6,0.7])
                vcontrol.throttle = 0.4
                vcontrol.brake = 0.0
                vcontrol.gear = 2
            else:
                self.auto_frame, self.man_frames = [np.random.choice([50,40,30]), np.random.choice([10,20,25])]              
