""" Functions to load/augment training dataset """
import tensorflow as tf
import numpy as np
import netCDF4 as nc

from typing import List, Tuple, Dict

def extract_array_data(file_path: str, args) -> np.ndarray:
  dataset = nc.Dataset(file_path, 'r')

  # number of ghost cells in x dimension
  gx = 2
  # extract vorticity and density without ghost cells and remove unit y direction
  var_arrays = []
  for var in args.variables:
      var_array = np.squeeze(dataset.variables[var][:,gx:-gx,:,:])
      var_arrays.append(var_array)
  dataset.close()

  flow_image = np.stack(var_arrays, axis=-1)
  return flow_image

def translate_augmentation(fields: Dict[str, tf.Tensor]) -> Dict[str, tf.Tensor]:
  coarse_image, error_image = fields['coarse'], fields['error']
  if coarse_image.shape != error_image.shape:
    raise ValueError(f"Coarse grained data and error should be same shape (got {coarse_image.shape} and {error_image.shape} respectively).")
  shape = tf.shape(coarse_image)
  nx, nz = shape[0], shape[1]
  shift_x = tf.random.uniform(shape=[], minval=0, maxval=nx-1, dtype=tf.int32)
  shift_z = tf.random.uniform(shape=[], minval=0, maxval=nz-1, dtype=tf.int32)

  # apply same shift to coarse snapshot and error
  coarse_shifted = tf.roll(coarse_image, shift_x, 0)
  coarse_shifted = tf.roll(coarse_shifted, shift_z, 1)
  error_shifted = tf.roll(error_image, shift_x, 0)
  error_shifted = tf.roll(error_shifted, shift_z, 1)
  return {'coarse': coarse_shifted, 'error': error_shifted}

def data_generator(ground_truth_file_names: List[str], coarse_grained_file_names: List[str], args):
  for gt_file, cg_file in zip(ground_truth_file_names, coarse_grained_file_names):
    raw_data_gt = extract_array_data(gt_file, args)
    raw_data_cg = extract_array_data(cg_file, args)[1:]
    error = raw_data_gt - raw_data_cg

    # Reshape tensors to have dynamic dimensions
    raw_data_cg = tf.convert_to_tensor(raw_data_cg, dtype=tf.float64)
    error = tf.convert_to_tensor(error, dtype=tf.float64)
    for i in range(raw_data_cg.shape[0]):
      yield {'coarse': raw_data_cg[i], 'error': error[i]}

def generate_augmented_dataset(
  ground_truth_file_names: List[str],
  coarse_grained_file_names: List[str],
  args,
) -> tf.data.Dataset:
  channels = len(args.variables)
  dataset = tf.data.Dataset.from_generator(
    lambda: data_generator(ground_truth_file_names, coarse_grained_file_names, args),
    output_signature={'coarse': tf.TensorSpec(shape=(None, None, channels), dtype=tf.float64),
    'error': tf.TensorSpec(shape=(None, None, channels), dtype=tf.float64)}
    )
  return dataset.map(translate_augmentation)
