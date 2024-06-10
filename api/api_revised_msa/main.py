# import requests
# import pyrebase
# from fastapi import FastAPI, HTTPException

firebase_config = {
    "apiKey": "AIzaSyAsBzpU1zgmBKwJzqchx-p6qkfzC7jVfDk",
    #"authDomain": "myapp.firebaseapp.com", 인증
    "projectId": "project-d3dfd",
    "storageBucket": "project-d3dfd.appspot.com",
    #"messagingSenderId": "123456789", #fcm
    "appId": "1:941985279122:android:fb20c0ef2ca7911006ca4b",
}

# firebase = pyrebase.initialize_app(firebase_config)
# fb_storage = firebase.storage()


# @app.post("/data")
# async def receive_data(request: Request):
#     try:
#         data = await request.json()
#         ref.push(data)
#         return JSONResponse(content={'status': 'success'}, status_code=200)
#     except Exception as e:
#         print(f"Failed to save data: {e}")
#         return JSONResponse(content={'status': 'failure'}, status_code=500)
import os
import torch
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, db
import uvicorn
from pydantic import BaseModel
from typing import Optional, List   
import numpy as np

app = FastAPI()

#admin sdk 실행 
cred = credentials.Certificate('project-d3dfd-firebase-adminsdk-walt9-7da718b3e7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-d3dfd-default-rtdb.asia-southeast1.firebasedatabase.app/',
})

#데이터 베이스모델
class Item(BaseModel):
    name: str
    description: Optional[str] = None


# @app.post("/censor/")
# async def create_item(item: Item):
#     new_item_ref = db.reference('censors').push(
#         # item.dict()
#         )
#     new_item_ref.set(item.model_dump())
#     return {"id": new_item_ref.key, **item.model_dump()}
def load_model(model_dir):
    model = torch.jit.load(os.path.join(model_dir, '2.pt'))
    model.to("cuda") if torch.cuda.is_available() else model.to("cpu")
    return model

def predict(ecg, model):
    
    if torch.cuda.is_available():
        ecg = ecg.to("cuda")
    output = model(ecg)
    
    
    output = output.squeeze().tolist()
    return output

def preprocess(ecg):
    
    # 리스트를 텐서로 변환

    ecg = torch.tensor(ecg)
    final_ecg = torch.reshape(ecg, (1, 96, 1))
    return final_ecg

model = load_model(".")

@app.get("/censor/{item_id}")
async def inference(item_id: str):
    item_ref = db.reference('censor').child(item_id)
    item = item_ref.get()
    if item:
        item = preprocess(item)
        item = predict(item, model)

        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#[-0.3796, 0.5715, -0.6271, -1.2358, 0.0664, 0.4190, 1.4306, 0.8688, -0.0335, 0.4487, 0.2255,0.1797, 0.4584, -0.7074, -0.3700, 0.1560, -0.2558, -0.2970, -0.6767, -0.2079,-0.4244, -0.1252, 0.1531, -0.5461, 0.7253, 0.5835, -0.5552, 0.2025, 0.4327, -0.0447, -0.1402, -0.4460, -0.8145,0.7082, 0.0675, -0.1314, 1.0965, 0.2283, -0.4741, -0.3172, -0.0852, 0.0898, -0.6138, -0.2715,0.2854, 1.1640, 1.2478, 0.7753, 0.0645, 1.3132, 1.3686, 0.0738, -0.4646, -0.1402, -0.6339,-0.1724, 0.5380, 0.2691, 0.2465, -0.6578, -0.5614, -0.4308, 0.5652, -0.3198, 0.0264, 0.0572, -0.5907, -0.1764, -0.2925, -0.1706, 0.6504, -0.1793, -0.1742, -0.6956, -1.3135, 0.3185, 0.5112, -0.9684, -0.0902, 0.3344, 0.9022, -0.6741, 0.9658, -1.1371, -0.3048, -0.6319, -0.2930, -1.3159, -0.2018, -0.2011, -0.5196, 0.3599, 0.0377, -0.2224, -0.4479, -0.9420]