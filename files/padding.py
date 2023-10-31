import tensorflow as tf
import numpy as np

from keras.engine.base_layer import Layer
from keras.engine.input_spec import InputSpec
from keras.utils import conv_utils

# some ideas here:
#  https://stackoverflow.com/questions/54911015/keras-convolution-layer-on-images-coming-from-circular-cyclic-domain

class CyclicPadding2D(Layer):
    def __init__(self, padding=(1, 1), data_format=None, **kwargs):
      super().__init__(**kwargs)
      self.data_format = conv_utils.normalize_data_format(data_format)
      if len(padding) != 2:
        raise ValueError('`padding` should have two elements. '
                         f'Received: {padding}.')
      self.padding = padding
      self.input_spec = InputSpec(ndim=4)

    def compute_output_shape(self, input_shape):
        input_shape = tf.TensorShape(input_shape).as_list()
        if self.data_format == 'channels_first':
          if input_shape[2] is not None:
            rows = input_shape[2]
          else:
            rows = None
          if input_shape[3] is not None:
            cols = input_shape[3] + self.padding[0] + self.padding[1]
          else:
            cols = None
          return tf.TensorShape(
            [input_shape[0], input_shape[1], rows, cols])
        elif self.data_format == 'channels_last':
          if input_shape[1] is not None:
              rows = input_shape[1]
          else:
              rows = None
          if input_shape[2] is not None:
              cols = input_shape[2] + self.padding[0] + self.padding[1]
          else:
              cols = None
          return tf.TensorShape([input_shape[0], rows, cols, input_shape[3]])

    def call(self, inputs):
        if self.data_format == "channels_last":
            #(batch, rows, cols, channels)
            axis = 2
            return tf.concat([
                inputs[:,:,-self.padding[0]:,:], 
                inputs,
                inputs[:,:,:self.padding[1],:]
            ], axis)
        elif self.data_format == "channels_first":
            #(batch, channels, rows, cols)
            axis = 3
            return tf.concat([
                inputs[:,:,:,-self.padding[0]:], 
                inputs,
                inputs[:,:,:,:self.padding[1]]
            ], axis)
