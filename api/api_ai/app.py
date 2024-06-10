# 

import json
import os
import ast
import torch
import numpy as np
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

class Payload(BaseModel):
    input: List[float]
    

def load_model(model_dir):
    model = torch.jit.load(os.path.join(model_dir, '2.pt'))
    model.to("cuda") if torch.cuda.is_available() else model.to("cpu")
    return model

def predict(ecg, model):
    
    if torch.cuda.is_available():
        ecg = ecg.to("cuda")
    output = model(ecg)
    
    
    output = { "ecg": output.squeeze().detach()}
    return output

def preprocess(ecg):
    ecg = torch.tensor(ecg)
    ecg = torch.reshape(ecg, (1, 96, 1))
    ecg = ecg.float()
    return ecg

def load_payload(payload : Payload):
    # payload = json.dumps(payload)
    # ecg = json.loads(payload)
    payload = payload.json()
    payload = ast.literal_eval(payload)
    # ecg = payload['input']
    return payload['input']

app = FastAPI()
model = load_model(".")


@app.get('/ping')
def pint():
    return "pong"

@app.post('/invocations')
async def invoke(payload : Payload):
    ecg = load_payload(payload)
    ecg = preprocess(ecg)
    output = predict(ecg, model)
    return output

@app.post("/load_payload")
async def load_payload(payload: Payload):
    # Pydantic 모델의 데이터를 받아서 처리합니다.
    input_data = payload.input
    # 데이터를 처리하는 로직을 여기에 추가합니다.
    # 예를 들어, 데이터를 데이터베이스에 저장하거나 다른 작업을 수행할 수 있습니다.
    
    return {"message": "Payload received", "input": input_data}
# list = [-0.3796, 0.5715, -0.6271, -1.2358, 0.0664, 0.4190, 1.4306, 0.8688, -0.0335, 0.4487, 0.2255,0.1797, 0.4584, -0.7074, -0.3700, 0.1560, -0.2558, -0.2970, -0.6767, -0.2079,-0.4244, -0.1252, 0.1531, -0.5461, 0.7253, 0.5835, -0.5552, 0.2025, 0.4327, -0.0447, -0.1402, -0.4460, -0.8145,0.7082, 0.0675, -0.1314, 1.0965, 0.2283, -0.4741, -0.3172, -0.0852, 0.0898, -0.6138, -0.2715,0.2854, 1.1640, 1.2478, 0.7753, 0.0645, 1.3132, 1.3686, 0.0738, -0.4646, -0.1402, -0.6339,-0.1724, 0.5380, 0.2691, 0.2465, -0.6578, -0.5614, -0.4308, 0.5652, -0.3198, 0.0264, 0.0572, -0.5907, -0.1764, -0.2925, -0.1706, 0.6504, -0.1793, -0.1742, -0.6956, -1.3135, 0.3185, 0.5112, -0.9684, -0.0902, 0.3344, 0.9022, -0.6741, 0.9658, -1.1371, -0.3048, -0.6319, -0.2930, -1.3159, -0.2018, -0.2011, -0.5196, 0.3599, 0.0377, -0.2224, -0.4479, -0.9420]

# payload = '{"input": [-0.3796, 0.5715, -0.6271, -1.2358, 0.0664, 0.4190, 1.4306, 0.8688, -0.0335, 0.4487, 0.2255,0.1797, 0.4584, -0.7074, -0.3700, 0.1560, -0.2558, -0.2970, -0.6767, -0.2079,-0.4244, -0.1252, 0.1531, -0.5461, 0.7253, 0.5835, -0.5552, 0.2025, 0.4327, -0.0447, -0.1402, -0.4460, -0.8145,0.7082, 0.0675, -0.1314, 1.0965, 0.2283, -0.4741, -0.3172, -0.0852, 0.0898, -0.6138, -0.2715,0.2854, 1.1640, 1.2478, 0.7753, 0.0645, 1.3132, 1.3686, 0.0738, -0.4646, -0.1402, -0.6339,-0.1724, 0.5380, 0.2691, 0.2465, -0.6578, -0.5614, -0.4308, 0.5652, -0.3198, 0.0264, 0.0572, -0.5907, -0.1764, -0.2925, -0.1706, 0.6504, -0.1793, -0.1742, -0.6956, -1.3135, 0.3185, 0.5112, -0.9684, -0.0902, 0.3344, 0.9022, -0.6741, 0.9658, -1.1371, -0.3048, -0.6319, -0.2930, -1.3159, -0.2018, -0.2011, -0.5196, 0.3599, 0.0377, -0.2224, -0.4479, -0.9420]}'
# list = load_payload(payload)
# ecg = preprocess(list)
# output = predict(ecg, model)
# print(output)