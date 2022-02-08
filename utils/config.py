# fvilmos, https://github.com/fvilmos
from utils.driver_type import DriverType
import cv2

# location of CARLA egg file
egg_file_abs_path = 'path to the .egg file'

# set driving mode
driver = DriverType()

#driver.set_driver_type(driver.autopilot)
#driver.set_driver_type(driver.inference)
driver.set_driver_type(driver.manual)
#driver.set_driver_type(driver.crazyautopilot)


# record data
record_data = False

# use out dit, to append to the "out" directory, the location to store recording
# use this for multiple scenario records, to organize your recordings
out_dir = "/map_uuu_x_2/"


#database name
db_name = '_info.rec'

# replace throtthel with a constant value
use_constant_thorttle = False
constant_thorttle = 0.40

# decide to load weights or a full model
use_weights = True

# model weights file
model_file='./ap.h5'

# number of predictions for steering model
NR_OF_PREDICTIONS=1

#head output elements
OUT_ELEMENTS=1

#number of image to process once
IMG_BUFF_LEN = 3


# network input dimensions
NETWORK_IN_WIDTH=160    
NETWORK_IN_HEIGHT=120
NETWORK_IN_CHANNELS=3

# built in map index
RANDOM_MAP = False
MAP_INDEX=4

# car will be spammed randomly on the map
RANDOM_START_POSITION=False

# car index, 36 = Audi, 10 = Mini
CAR_INDEX=36


# steering / throttle sensitivity
drive_increment = 0.1

# use this to define the record granurality
sensor_update_time = 0.08

# HUD font values
sizef = 0.5
typef = cv2.FONT_HERSHEY_SIMPLEX
color = [0,255,0]
sizeb = 1

# difference between waypoints - used to detect left / right turn
waypoint_diff = 0.15

# normalizer config
normalizer = {'img_mean':0,'img_std':255.0, 'velo_max':47.0, 'velo_min':0.0, 'velo_mean':16.73}

