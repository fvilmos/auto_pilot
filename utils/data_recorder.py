# fvilmos, https://github.com/fvilmos
import os
from datetime import datetime
class DataRecorder():
    def __init__(self, path='./', info_file_name='info.rec'):
        """
        Data Recorder class, records data.

        Args:
            path (string): absolut path to the directory to store data
            info_file_name (string): file to collect information from ego vehicle
        """
        self.path = path
        self.file_name = info_file_name
        self.count = 0
        self.record = False
    
    def enable_recording(self, val = False):
        if val == True:
            # open file for writeing
            try:
                # check if directory exists
                dir_exist = os.path.isdir(self.path)
                path = self.path
                if not dir_exist:        
                    os.mkdir(self.path)
                else:
                    #create a dir from timestamp
                    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    dir_name = os.path.join(self.path,ts)
                    os.mkdir(dir_name)
                    path = dir_name + '/'
                    self.path = path
                self.f = open(path + self.file_name,'w')
                #self.record = True
                print ("save path:" + path + self.file_name)
                return path

            except :
                print ('something went wrong...check filename, path, or if directory allready exists!')

    
    def save_sensor_data(self,file_name_dict,vcontrol=None,velo=0.0,direction='',junction=0,waypoint=""):
        """
        Call periodically to collect data
        Args:
            file_name_dict (dict): holds the image name (rgb / drgb)
            vcontrol ( VehicleControl, optional): Carla VehicleControl object. Defaults to None.
            velo (float, optional): Velocity [km/h]. Defaults to 0.0.
        """
        infoline = ''

        if self.record:
            # record if we have all date from the sensors
            try:
                # collect file names
                rgb_c = file_name_dict['rgb']
                depth_c = file_name_dict['depth']

                infoline = '{ "index": '+ str(self.count) \
                    + ',' + '"throttle": ' + '{:.2f}'.format(vcontrol.throttle) \
                    + ',' + '"steer": ' + '{:.2f}'.format(vcontrol.steer) \
                    + ',' + '"brake": ' + '{:.2f}'.format(vcontrol.brake) \
                    + ',' + '"hand_brake": ' + '"' + str(vcontrol.hand_brake) + '"' \
                    + ',' + '"reverse": ' + '"' + str(vcontrol.reverse) + '"' \
                    + ',' + '"manual_geat_shift": ' + '"' + str(vcontrol.manual_gear_shift) + '"' \
                    + ',' + '"gear": ' + '{:.2f}'.format(vcontrol.gear) \
                    + ',' + '"velo": ' + '{:.1f}'.format(velo) \
                    + ',' + '"direction": ' + '"' + str(direction) + '"' \
                    + ',' + '"junction": ' + '{}'.format(str(junction)) \
                    + ',' + '"waypoint": ' + '{}'.format(str(waypoint)) \

                infoline += ',' + '"rgb_c": ' + '"' + str(rgb_c) + '"'
                infoline += ',' + '"depth_c": ' + '"'+ str(depth_c) + '"'
                infoline += '} \n'

                self.f.write(infoline)
                print ("index: " + str(self.count) + " direction: " + str(direction) + "\n")
                self.count += 1

            except:
                # not all data avaialble, skipp
                pass

    def close_file(self):
        """
        Close file object
        """
        if self.record:
            self.f.close