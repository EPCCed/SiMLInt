import sys

from smartredis import Client
from smartsim import Experiment

import numpy as np


db_port = int(sys.argv[1])
#model_path = '/work/d175/shared/zero-model-256.pb'
model_path = sys.argv[2]

exp = Experiment("Inference-Test", launcher="local")

db = exp.create_database(port=db_port, interface="lo")
exp.start(db)

print(f'Started Redis database at {db.get_address()[0]}')

# these need to match the outputs from 'write_zero_model.py'
inputs = ['args_0']
outputs = ['Identity']

client = Client(address=db.get_address()[0], cluster=False)

client.set_model_from_file(
    "hw_zero_model", model_path, "TF", device="CPU", inputs=inputs, outputs=outputs
)
print('Uploaded model')

