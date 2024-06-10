# 

import requests
import pyrebase
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

firebase_config = {
    "apiKey": "AIzaSyD1J9Q9J9J9J9J9J9J9J9J9J9J9J9J9J9",
    "authDomain": "myapp.firebaseapp.com",
    "projectId": "myapp",
    "storageBucket": "myapp.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "1:123456789:web:123456789",
}

firebase = pyrebase.initialize_app(firebase_config)
fb_storage = firebase.storage()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, db
import uvicorn

app = FastAPI()

cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

ref = db.reference('sensor_data')

@app.post("/data")
async def receive_data(request: Request):
    try:
        data = await request.json()
        ref.push(data)
        return JSONResponse(content={'status': 'success'}, status_code=200)
    except Exception as e:
        print(f"Failed to save data: {e}")
        return JSONResponse(content={'status': 'failure'}, status_code=500)

@app.post("/items/")
async def create_item(item: Item):
    new_item_ref = db.reference('items').push(
        # item.dict()
        )
    new_item_ref.set(item.model_dump())
    return {"id": new_item_ref.key, **item.model_dump()}
