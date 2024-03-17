# %%writefile app.py
from flask import Flask
from PIL import Image
from engine import vit, isolationforest

app = Flask(__name__)


allowed_data_extension  = {'png','jpeg','jpg'} #edf,rml 변환
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_data_extension
@app.route('/predict',methods =['GET'])
def prediction():


# export FLASK_APP = main.py
# export FLASK_DEBUG= 1
# flask run
#postman에 서버주소 입력 api 관리
