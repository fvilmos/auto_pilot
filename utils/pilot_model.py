# fvilmos, https://github.com/fvilmos

from tensorflow import keras
import numpy as np
import tensorflow as tf
from utils.switch_layer import SwitchLayer

class PilotModel():
    __instance = None
    __model = None
    '''
    Singleton class, model is only created at stratup
    '''
    def __init__(self,iwith=320,iheight=60,channels=3, velocity=1,direction=1,nr_of_predictions=10, weights_file=None, img_buff_len=3):
        
        if PilotModel.__instance == None:
            PilotModel.__instance = self

            # create and load model
            PilotModel.__model = PilotModel.__get_model_3D_CNN(iwith,iheight,channels,velocity,direction,nr_of_predictions=nr_of_predictions, img_buffer_len=img_buff_len)
            
            if weights_file is not None:
                print (weights_file)
                PilotModel.load_model_weights(weights_file)
    
    @staticmethod  
    def get_model():
        '''
        Return the model only
        '''
        return PilotModel.__model
    
    
    @staticmethod  
    def load_model_weights(fweights='weights.hdf5'):
        '''
        Load weights file
        '''
        PilotModel.__model.load_weights(fweights)
    
    
    @staticmethod
    def clean_instance():
        '''
        Reset model
        '''
        PilotModel.__instance = None
    
    @staticmethod
    def __get_model_3D_CNN(iwith=320,iheight=60,channels=3, velocity=1,direction=1,nr_of_predictions=15, img_buffer_len=3):    

        vector_dir = keras.layers.Input(shape=(direction,), name="cmd_in", dtype='int32')
        img_in3D = keras.layers.Input(shape=(img_buffer_len, iheight, iwith, channels), name='img_in')
        
        x = img_in3D

        #crop
        x = keras.layers.Cropping3D(cropping = ((0, 0),(iheight//2, 0),(0, 0)))(x)


        # normalize
        x = keras.layers.Lambda(lambda x: x / 127.0 - 1.0)(x)  # normalize

        x = keras.layers.Convolution3D(4, (3, 3, 3) ,strides=(1, 2, 2),name='conv3d_l1')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation(keras.activations.elu)(x)
        x = keras.layers.MaxPooling3D(pool_size=(1, 2, 2))(x)

        x = keras.layers.Dropout(0.4)(x) # 0.4
        
        x = keras.layers.Convolution3D(96, (6, 6, 6), strides=(2, 2, 2), padding="SAME",name='conv3d_l2')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation(keras.activations.elu)(x)
        x = keras.layers.MaxPooling3D(pool_size=(2, 2, 2), padding="SAME")(x)
     
        x = keras.layers.Dropout(0.4)(x) # 0.4
        
        x = keras.layers.Convolution3D(16, (5, 5, 5), strides=(2, 2, 2), padding="SAME",name='conv3d_l3')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation(keras.activations.elu)(x)
        x = keras.layers.MaxPooling3D(pool_size=(2, 2, 2), padding="SAME")(x)
         
        x = keras.layers.Dropout(0.3)(x) #0.3
        
        x = keras.layers.Flatten(name='flattened')(x)
        
        #===================== velo ==========================
        vector_velo = keras.layers.Input(shape=(velocity,), name="velo_in")
        velo = keras.layers.Lambda(lambda x: x / 10.0)(vector_velo)
        #out_velo = keras.layers.Dense(5, name='out_velo_0')(velo)
        velo = keras.layers.Dense(20, name='d_out_velo_0')(velo)
        velo = keras.layers.BatchNormalization()(velo)
        out_velo = keras.layers.Activation(keras.activations.elu,name='out_velo_0')(velo)
        
        # Concatenate the convolutional features and the vectors
        x = keras.layers.Concatenate()([x,out_velo])
        
        x = keras.layers.Dense(150,use_bias=True)(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.activations.elu(x)
        
        x_v = keras.layers.Dense(256,use_bias=True)(x)
        x_v = keras.layers.BatchNormalization()(x_v)
        x_v = keras.activations.elu(x_v)
        
        
        x_th = keras.layers.Dense(64,use_bias=True)(x)
        x_th = keras.layers.BatchNormalization()(x_th)
        x_th = keras.activations.elu(x_th)

        #======================== branching =================================
        out_steer = []
        out_throttle = []

        x_v = SwitchLayer(64,4)([x_v,vector_dir])
        
        x_v = SwitchLayer(16,4)([x_v,vector_dir])
        x_v = SwitchLayer(4,4)([x_v,vector_dir])
        x_v = SwitchLayer(1,4,name='steer_out_0')([x_v,vector_dir])
        
        x_th = SwitchLayer(16,4)([x_th,vector_dir])
        x_th = SwitchLayer(4,4)([x_th,vector_dir])
        x_th = SwitchLayer(1,4, name='throttle_out_0')([x_th,vector_dir])

        
        out_steer.append(x_v)
        out_throttle.append(x_th)
        
        
        # create name list
        dnames = [] 
        [dnames.append("steer_out_{}".format(i)) for i in range(nr_of_predictions)]
        [dnames.append("throttle_out_{}".format(i)) for i in range(nr_of_predictions)]
        
        # create values list
        dvals = []
        [dvals.append(out_steer[i]) for i in range(nr_of_predictions)]
        [dvals.append(out_throttle[i]) for i in range(nr_of_predictions)]
        
        # join the lists, create a dict
        d_out = dict(zip(dnames,dvals))

        model = keras.Model(inputs=[img_in3D,vector_dir,vector_velo], outputs=d_out)

        m_loss = []
        [m_loss.append("steer_out_{}".format(i)) for i in range(nr_of_predictions)]
        [m_loss.append("throttle_out_{}".format(i)) for i in range(nr_of_predictions)]
        
        # create values list
        m_loss_vals = []
        #[m_loss_vals.append("huber_loss") for i in range(nr_of_predictions)]
        [m_loss_vals.append("mean_absolute_error") for i in range(nr_of_predictions)]
        [m_loss_vals.append("mean_absolute_error") for i in range(nr_of_predictions)]
        
        # join the lists, create a dict
        m_loss_out = dict(zip(m_loss,m_loss_vals))
        
        steer_w = 0.95/nr_of_predictions
        throttle_w = 0.05/nr_of_predictions
        
        
        m_weights = []
        [m_weights.append("steer_out_{}".format(i)) for i in range(nr_of_predictions)]
        [m_weights.append("throttle_out_{}".format(i)) for i in range(nr_of_predictions)]
        
        
        # create values list
        m_weights_vals = []
        [m_weights_vals.append(steer_w) for i in range(nr_of_predictions)]
        [m_weights_vals.append(throttle_w) for i in range(nr_of_predictions)]
        

        
        # join the lists, create a dict
        m_weights_out = dict(zip(m_weights,m_weights_vals))
        
        opti = keras.optimizers.RMSprop()
        #opti = keras.optimizers.Adagrad(learning_rate=0.01)

        keras.utils.plot_model(model, "model.png",show_shapes=True)
        
        model.compile(optimizer=opti, loss=m_loss_out, loss_weights=m_weights_out,metrics=['mae'])
        return model

