# fvilmos, https://github.com/fvilmos
import tensorflow.keras as keras
import tensorflow as tf

class SwitchLayer(keras.layers.Layer):
    def __init__(self, nr_output_neurons, nr_command_signals, **kwargs):
        tf.config.experimental_run_functions_eagerly(True)
        super().__init__(**kwargs)
        self.nr_output_neurons = nr_output_neurons
        self.nr_command_signals = nr_command_signals
                    
    def build(self, input_shape):
        super().build(input_shape)
        self.trainable = True
        
    def call(self, inputs):
        # decode command, from symbolic tensor
        return keras.layers.Lambda(lambda x: keras.backend.switch(keras.backend.equal(inputs[1],0),self.switch_layer(inputs[0],0, self.nr_output_neurons,self.nr_command_signals)\
                                                                  ,keras.backend.switch(keras.backend.equal(inputs[1],1), self.switch_layer(inputs[0],1, self.nr_output_neurons,self.nr_command_signals),\
                                                                   keras.backend.switch(keras.backend.equal(inputs[1],2), self.switch_layer(inputs[0],2, self.nr_output_neurons,self.nr_command_signals), \
                                                                                        self.switch_layer(inputs[0],3, self.nr_output_neurons,self.nr_command_signals) ))))(inputs)

    
    #@staticmethod
    def switch_layer(self,in_layer, command, nr_output_neurons,nr_command_signals):
    
        # compute the nr of out layer, based on the control number
        # i.e. in_layer full shape [None, 768], nr of commands = 3
        # out layer shape is 768//3== 256 out x 3 commands
        # Reshape (256,3), this MUST be the same with the nr_output_neurons and nr_command_signals
        # defined in the __init__ function
        val= keras.layers.Reshape((nr_output_neurons,nr_command_signals))(in_layer)
        
        # we get a array of shape [None,256,3]
        # once we need just [None,256], selected by the command
        
        return val[:,:,command]
    