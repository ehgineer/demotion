import requests
import json
from PIL import Image
import numpy as np


def prediction_req(image_path):
    # 우리 신경망은 입력으로 바이트스트림이 아니라 행렬 형태로 데이터를 받는다.
    # 따라서 이미지를 96x96 크기의 행렬로 변환
    
    img_width, img_height =128, 128
    
    img = Image.open(image_path)
    img_resized = img.resize(size=(img_width, img_height))
    img_arr_fmt = np.expand_dims(np.asarray(img_resized), axis=0)
   
    # 넘파이 행렬을 파이썬 기본 리스트 자료형으로 변환해 API 입력 형식으로 변환 
    predict_req = {"instances":np.vstack([img_arr_fmt]).tolist() } 
    data = json.dumps(predict_req)
    
    
    # 엔드포인트 지정
    print('\n==start==')
    endpoint = "http://35.229.210.35:880/v1/models/dog_model:predict"
    print(f'endpoint: {endpoint}')
    
    # 엔드포인트에 행렬로 변환한 이미지를 POST로 요청
    res = requests.post(url=endpoint, data=data)
    json_res = json.loads(res.text)
        
    # 예측 출력을 취함
    classes = json_res['predictions']
    
    # 출력값 중 가장 높은 값을 프린트
    print(str(np.argmax(classes)))
    print('==end==')
    
    # 출력값 리턴
    return str(np.argmax(classes))