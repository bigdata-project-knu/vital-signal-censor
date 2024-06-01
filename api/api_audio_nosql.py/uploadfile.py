from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
import uvicorn 
import json

# Init App
app = FastAPI()

@app.post("/file/upload")
def upload_file(file: UploadFile):
    if file.content_type != "application/json":
        raise HTTPException(400,detail="Invalid document type")
    else:
        data = json.loads(file.file.read())
    return {"content":data ,"filename":file.filename}


if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)