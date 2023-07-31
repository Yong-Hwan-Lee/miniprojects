import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import time
plt.style.use('dark_background')

esp32_ip = "http://192.168.0.116"

response = requests.get(esp32_ip + "/capture")

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_notebook(notebook_path):
    # Jupyter Notebook 파일(.ipynb)을 읽어옴
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 코드 실행 프로세서 생성
    ep = ExecutePreprocessor(timeout=-1)  # -1은 타임아웃을 설정하지 않음을 의미

    # 코드 실행
    ep.preprocess(nb, {'metadata': {'path': './'}})


if response.status_code == 200:
    with open("capture.jpg", "wb") as f:
        f.write(response.content)
    print("Image caputure successfully.")
    notebook_path = 'cartest.ipynb'  # 실행시키려는 Jupyter Notebook 파일 경로를 입력
    execute_notebook(notebook_path)
    print("차량 인식완료")
  

    time.sleep(1)
    

else:
     print("Failed to capture image.")