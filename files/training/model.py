from tensorflow.keras.layers import Input, Normalization, Conv2D
from tensorflow.keras import Model
from tensorflow import keras
from typing import Tuple

import padding

'''
preprocessing:

- "cyclic" padding along the flow direction (wall dimension is 0-padded):
    the input padded with   2 columns on both sides that 'wrap' around (see np.pad('wrap'))
                            two rows of 0 on top and bottom
    ! needs to be reapplied after every convolution layer
'''

'''
TODO/preprocessing:

- rescale input to [-1, 1]:
    To rescale an input in the [0, 255] range to be in the [-1, 1] range, 
        you would pass scale=1./127.5, offset=-1.
        in general: scale = scaled_max/(max * .5) 
                    offset = min + scaled_min
    keras.layers.Rescaling(scale, offset=0.0, **kwargs)

    keras seems not to support min-max scaling with variable min/max, so will normalise instead
'''

def kochkov_cnn(image_shape: Tuple[int]) -> keras.Model:
  """ Todo: need a more automated way of padding e.g. if we adjust filter size. """
  model = keras.Sequential()

  model.add(Input(shape=image_shape))

  #1
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
#  model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters=64, kernel_size=3, padding ='valid', activation='relu'))

  #2
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
#  model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters =64, kernel_size =3, padding ='valid', activation='relu'))

  #3
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
#  model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters =64, kernel_size =3, padding ='valid', activation='relu'))

  #4
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
#  model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters =64, kernel_size =3, padding ='valid', activation='relu'))

  #5
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
#  model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters =64, kernel_size =3, padding ='valid', activation='relu'))

  #6
  # pad
  model.add(padding.CyclicPadding2D(padding=(1,1)))
 # model.add(keras.layers.ZeroPadding2D(padding=(1,0)))

  model.add(Conv2D (filters =64, kernel_size =3, padding ='valid', activation='relu'))

  # output
  model.add(padding.CyclicPadding2D(padding=(1,1)))

  model.add(Conv2D(filters=image_shape[2], kernel_size =3, padding ='valid', activation='linear'))
  return model
