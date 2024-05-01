""" Setup training loop for basic model """
import tensorflow as tf
import model
import data_read as dr
from model import kochkov_cnn
from datetime import datetime
import argparse

# monitoring and debugging through tensorboard
#log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
#tf.debugging.experimental.enable_dump_debug_info(log_dir, tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1)

tf.keras.utils.disable_interactive_logging()

parser = argparse.ArgumentParser(description='Model training')
parser.add_argument('-lr', '--learning-rate', type=float, required=True)
parser.add_argument('-b', '--batch-size', type=int, required=True)
parser.add_argument('-ep', '--epochs', type=int, required=True)
parser.add_argument('-id', '--task-id', default='')
parser.add_argument('--vort-only', action='store_true',)
parser.add_argument('--dens-only', action='store_true',)
args = parser.parse_args()

# problem size
Nx = 256
Nz = 256
if args.vort_only or args.dens_only:
  channels = 1
else:
  channels = 2
val_frac = 0.2

samples_per_file = 1000 # to estimate train/val split
#data_location = '/scratch/space1/d175/data/training/derived/notebooks/'
data_location = '/work/d175/d175/akexcml/smartsim/python/data/'
file_nums = list(range(1,33)) # [ x+1 for x in range(32) ]

# training protocol
#learning_rate = 1e-3
#epochs = 2
#batch_size = 32
learning_rate = args.learning_rate
epochs = args.epochs
batch_size = args.batch_size

trun_label = datetime.now().strftime("%Y%m%d-%H%M%S")
if args.task_id:
    trun_label = f'{trun_label}-{args.task_id}'
log_dir = f"logs/fit/{trun_label}"
checkpoint_filepath = 'checkpoints/' + trun_label + '/weights.{epoch:03d}.hdf5'

print('****************************************************')
print(f'learning rate: {learning_rate}')
print(f'epochs:        {epochs}')
print(f'batch size:    {batch_size}')
print(f'training run:  {trun_label}')
print(f'data files:    {file_nums}')
print(f'channels:      {channels}', end='')
if args.vort_only:
  print(' (vort)')
elif args.dens_only:
  print(' (dens)')
else:
  print('')
print('****************************************************')

# compile model
model = kochkov_cnn((Nx, Nz, channels))
model.summary()
model.compile(loss='mean_squared_error', run_eagerly=False, jit_compile=False, optimizer=tf.keras.optimizers.Adam(jit_compile=False))

# error = gt - sim
# load ground truth (gt) and coarse-grained (='sim', cg)
file_paths_gt = [data_location + 'gt_traj_' + str(n) + '.nc' for n in file_nums]
file_paths_cg = [data_location + 'sim_traj_' + str(n) + '.nc' for n in file_nums]
n_samples = samples_per_file * len(file_paths_cg)

# generate dataset (from generator, data not preloaded)
dataset = dr.generate_augmented_dataset(file_paths_gt, file_paths_cg, args)
dataset = dataset.shuffle(buffer_size=100)
dataset.prefetch(batch_size)

# split the dataset into training and validation sets
train_size = int(n_samples * (1 - val_frac))
val_size = n_samples - train_size
train_dataset = dataset.take(train_size)
val_dataset = dataset.skip(train_size)

# training
def input_and_target(sample):
  """ Ensure data is correctly sized and split into input/target """
  return (
    tf.image.resize(sample['coarse'], (Nx, Nz)),
    tf.image.resize(sample['error'], (Nx, Nz))
  )

# batch the training and validation datasets
train_dataset = train_dataset.map(input_and_target).batch(batch_size)
val_dataset = val_dataset.map(input_and_target).batch(batch_size)

# monitor training through tensorboard
#tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
#tf.debugging.experimental.enable_dump_debug_info(log_dir, tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1)

# checkpoint weights after each epoch
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
)

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=[
#        tensorboard_callback,
        model_checkpoint_callback,
    ],
)
for key in history.history.keys():
    print(key)
    print(history.history[key])

print('***************************************')
print('Freeze model: ', end='')
try:
    # try if smartsim is available
    from smartsim.ml.tf import freeze_model
    print('Using smartsim')
except:
    print('Failed to load smartsim, using tf_utils')
    from tf_utils import freeze_model
import os

model_path, inputs, outputs = freeze_model(model, os.getcwd(), f"model-hw-{trun_label}.pb")
print(model_path)
print(inputs)
print(outputs)
print('***************************************')
