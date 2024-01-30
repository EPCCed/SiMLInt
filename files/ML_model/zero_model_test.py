from smartredis import Client
from smartsim import Experiment

import numpy as np

exp = Experiment("Inference-Test", launcher="local")

db = exp.create_database(port=6899, interface="lo")
exp.start(db)

print(db.get_address())

model_path = '/path/to/zero-model-xxx-zzz.pb'
inputs = ['args_0']
outputs = ['Identity']

client = Client(address=db.get_address()[0], cluster=False)

client.set_model_from_file(
    "keras_fcn", model_path, "TF", device="CPU", inputs=inputs, outputs=outputs
)

# put random random input tensor into the database
input_data = np.random.rand(1, 260, 256, 1).astype(np.float64) 
client.put_tensor("input", input_data)

# run the Fully Connected Network model on the tensor we just put
# in and store the result of the inference at the "output" key
client.run_model("keras_fcn", "input", "output")

# get the result of the inference
pred = client.get_tensor("output")
print(pred)

exp.stop(db)
