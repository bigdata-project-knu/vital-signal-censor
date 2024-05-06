from Datareading import temp
from helpers import parse_response

import asyncio
from fastapi import FastAPI, HTTPException
import ast

app = FastAPI(
    title="Log data client"
)



@app.get("/ecg")
async def main():
    # try: 
    try:   
        data = await temp()
        json_str = ast.literal_eval(data)
        temparature=json_str["ecg"]
        out ={
            "hr":temparature["hr"],
            "hrv":temparature["hrv"],
            "value":temparature["value"]
            }
    except:
        data = await temp()
        print(data)
        if data == None:
            out ={
            "hr":0,
            "hrv":0,
            "value":0
            }
        else:
            out = parse_response(data)
            out = data
    return out
