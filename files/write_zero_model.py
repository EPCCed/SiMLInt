import argparse
import os

parser = argparse.ArgumentParser(
             prog='write_zero_model.py',
             description='Write a model that produces zero to a file')
parser.add_argument('x', help='grid size x', type=int)
parser.add_argument('z', help='grid size z', type=int)
parser.add_argument('-f', '--filename', help='output filename', required=True)
args = parser.parse_args()


from smartsim.ml.tf import freeze_model

from tensorflow.keras.layers import Input, Normalization, Conv2D
from tensorflow.keras import Model
from tensorflow import keras
import tensorflow as tf

tf.keras.backend.set_floatx('float64')

import padding

import numpy as np

model = keras.Sequential()

model.add(Input(shape=(args.x, args.z, 1)))

#1
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D (filters=64, kernel_size=3, padding='valid', activation='relu'))

#2
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D (filters=64, kernel_size=3, padding='valid', activation='relu'))

#3
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D(filters=64, kernel_size=3, padding='valid', activation='relu'))

#4
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D (filters=64, kernel_size=3, padding ='valid', activation='relu'))
#model.add(Normalization(axis=-1, mean=None, variance=None))\

#5
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D (filters=64, kernel_size=3, padding='valid', activation='relu'))
#model.add(Normalization(axis=-1, mean=None, variance=None))\

#6
# pad
model.add(padding.CyclicPadding2D(padding=(1,1)))
model.add(keras.layers.ZeroPadding2D(padding=([(1,1), (0,0)])))

model.add(Conv2D (filters=64, kernel_size=3, padding ='valid', activation='relu'))

model.add(Conv2D (filters=1, kernel_size=3, padding ='same', activation='relu'))

model.summary()

model.compile(
    # Optimizer
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    # Loss function to minimize
    loss=keras.losses.MeanSquaredError()
    # List of metrics to monitor
    #metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

last_layer = len(model.layers) - 1
zero_weights = [tf.zeros(shape=(3,3,64,1)), tf.zeros(shape=(1,))]
model.layers[last_layer].set_weights(zero_weights)

# SmartSim utility for Freezing the model and saving it to a file.
model_path, inputs, outputs = freeze_model(model, os.getcwd(), args.filename)

print(model_path)
print(inputs)
print(outputs)
