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

if __name__ == '__main__':
    notebook_path = 'cartest.ipynb'  # 실행시키려는 Jupyter Notebook 파일 경로를 입력
    execute_notebook(notebook_path)
