from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ask")
def ask(text:str,image  ):
    content = image.file.read()

    #image = Image(io.BytesIO(content))
    image = Image(image.file)

    result = model_pipeline(text, image)
    return result

# def api_middleware(app: FastAPI):
#     rich_available = False
#     try:
#         if os.environ.get('WEBUI_RICH_EXCEPTIONS', None) is not None:
#             import anyio 
#             import starlette 
#             from rich.console import Console
#             console = Console()
#             rich_available = True
#     except Exception:
#         pass

#api endpoint 구하기
def url(url : str):
    import socket
    from ... import urlparse
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        ipaddress = domain.split('.')[1]
        ip = ipaddress.
    
