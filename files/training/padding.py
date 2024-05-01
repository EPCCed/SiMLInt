import tensorflow as tf

# from keras.engine.base_layer import Layer
# from keras.engine.input_spec import InputSpec
# from keras.utils import conv_utils
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import InputSpec
from tensorflow.python.keras.utils import conv_utils

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

    def get_config(self):
        config = super().get_config()
        config.update({
            "padding": self.padding,
            "data_format": self.data_format,
        })
        return config

    def compute_output_shape(self, input_shape):
        input_shape = tf.TensorShape(input_shape).as_list()
        if self.data_format == 'channels_first':
          if input_shape[2] is not None:
            rows = input_shape[2] + 2 * self.padding[0]
          else:
            rows = None
          if input_shape[3] is not None:
            cols = input_shape[3] + 2 * self.padding[1]
          else:
            cols = None
          return tf.TensorShape(
            [input_shape[0], input_shape[1], rows, cols])
        elif self.data_format == 'channels_last':
          if input_shape[1] is not None:
              rows = input_shape[1] + 2 * self.padding[0]
          else:
              rows = None
          if input_shape[2] is not None:
              cols = input_shape[2] + 2 * self.padding[1]
          else:
              cols = None
          return tf.TensorShape([input_shape[0], rows, cols, input_shape[3]])

    def call(self, inputs):
        tensor = inputs
        ndim = len(inputs.shape)
        for ax, pd in enumerate(self.padding):
            if self.data_format == "channels_last":
                #(batch, rows, cols, channels)
                axis = 1 + ax
            elif self.data_format == "channels_first":
                #(batch, channels, rows, cols)
                axis = 2 + ax
            else:
                return
            sl_start = [slice(None, pd) if i == axis else slice(None) for i in range(ndim)]
            sl_end = [slice(-pd, None) if i == axis else slice(None) for i in range(ndim)]
            tensor = tf.concat([
                tensor[sl_end],
                tensor,
                tensor[sl_start],
            ], axis)

        return tensor
