import os
import ast
import torch
import numpy as np
from typing import List

from pydantic import BaseModel
from torchvision import transforms
# from PIL import Image

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter



# router = APIRouter(
#     prefix="/AI_MODEL",
#     tags=['AI_MODEL']
# )


class ECGdata(BaseModel):
    input: List[float]

def load_model(model_dir):
    model = torch.jit.load(os.path.join(model_dir, 'model.pt'))
    model.to("cuda") if torch.cuda.is_available() else model.to("cpu")
    return model

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ECGData)
def process(input : schemas.ECGData, model):
    if torch.cuda.is_available():
      ecg = ecg.to("cuda")
    output = model(ecg)
    return output
    


#if 이미지
# def predict(preprocessed_image, model):
#     preprocessed_image = preprocessed_image.unsqueeze(0)
#     if torch.cuda.is_available():
#         preprocessed_image = preprocessed_image.to("cuda")
#     log_probs = model(preprocessed_image)
#     probs = torch.softmax(log_probs, dim=1)
#     proba, class_ = torch.max(probs, dim=1)
#     output = {'class': class_.detach().cpu().numpy().item(), 
#               'proba': proba.detach().cpu().numpy().item()}
#     return output


app = FastAPI()
model = load_model(".")


@app.get('/ping')
def pint():
    return "pong"

