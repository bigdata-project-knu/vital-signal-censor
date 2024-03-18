# %%writefile app.py
from flask import Flask, request, jsonify
from PIL import Image
from engine import vit, isolationforest
from isolationforest implement import get_prediction
import os
from PIL import Image

app = Flask(__name__)


allowed_data_extension  = {'png','jpeg','jpg'} #edf,rml 변환
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_data_extension
@app.route('/predict',methods =['POST','GET'])
    def prediction():
        if request.method == 'POST':
            file = request.files.get('file')
            if file is None or file.filename == '':
                return jsonify({'error': '파일 없음'})
            if not is_allowed_file(file.filename):
                return jsonify({'error': '지원하지 않는 파일형식'})
            try:
                img_bytes = file.read() #jpeg, png파일을 바이트로
                img_tensor = transform_image(img_bytes) # 이미지를 tensor형태로 바꿈
                prediction = get_prediction(img_tensor) #정상 0, 이상 1
                data = {'prediction':prediction.item()}
                return jsonify(data)
            except e:
                return jsonify({'error':'ai 파이프라인 오류'})
        return jsonify({'결과':'수행 종료'})
                

# export FLASK_APP = main.py
# export FLASK_DEBUG= 1
# flask run
#postman에 서버주소 입력 api 관리
