# 


import os
import ast
import torch
import numpy as np
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

class Payload(BaseModel):
    input: List[List[float]]
    

def load_model(model_dir):
    model = torch.jit.load(os.path.join(model_dir, '2.pt'))
    model.to("cuda") if torch.cuda.is_available() else model.to("cpu")
    return model

def predict(ecg, model):
    
    if torch.cuda.is_available():
        ecg = ecg.to("cuda")
    output = model(ecg)
    
    
    output = { ecg:output.squeeze().numpy()}
    return output

def preprocess(ecg):
    ecg = torch.tensor(ecg)
    final_ecg = torch.reshape(ecg, (1, 96, 1))
    return final_ecg

def load_payload(payload: Payload):
    payload = payload.json()
    payload = ast.literal_eval(payload)
    ecg = payload['input']
    return ecg

app = FastAPI()
model = load_model(".")


@app.get('/ping')
def pint():
    return "pong"

@app.post('/invocations')
def invoke(payload: Payload):
    ecg = load_payload(payload)
    ecg = preprocess(ecg)
    output = predict(ecg, model)
    return output