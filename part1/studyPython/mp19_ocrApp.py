# 글자 추출
# 이미지 처리 모듈 pip install pillow
# OCR 모듈 pip install pytesseract
# Tesseract-OCR 컴퓨터 설치
from PIL import Image
import pytesseract as tess 

img_path = './studyPython/65노0887.jpg'
tess.pytesseract.tesseract_cmd = 'C:/DEV/Tools/Tesseract-OCR/tesseract.exe'

result = tess.image_to_string(Image.open(img_path), lang = 'kor')
print(result)

