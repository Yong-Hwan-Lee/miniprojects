
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)  
        # 검색어 입력후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row, column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 1).text()
        webbrowser.open(url) # 뉴스기사 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '검색으로르 입력하세요!')
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'news' # movie로 변경하면 영화검색
        #    outputs = [] # 결과 담을 리스트변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # 테이블위젯에 출력 기능
            items = result['items'] # json결과 중  items 아래 배열만 추출
            self.makeTable(items)

    #테이블 위젯에 데이터표시
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일 선택
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(items)) # 현재 100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblResult.setColumnWidth(0, 310)
        self.tblResult.setColumnWidth(1, 260)
        # 컬럼 데이터를 수정금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 ....
            # num = i + 1 # 뉴스번호
            title = self.replaceHtmlTag(post['title']) # HTMl 특수문자 변환
            originallink = post['originallink']
            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))

    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;', '<')
        result = result.replace('&gt;', '>')  
        result = result.replace('<b>', '') 
        result = result.replace('</b>', '')
        result = result.replace('&apos;', "'")  
        result = result.replace('&quot;', '"')  
        # 변환 안된 특수문자가 나타나면 여기 추가  # lesser than 작다 greater than 크다 bold apostrophe 홑따옴표 quotation mark 쌍따옴표

        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())