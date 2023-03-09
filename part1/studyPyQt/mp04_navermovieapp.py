import sys
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * #QIcon
from NaverApi import *
from urllib.request import urlopen
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApimovie.ui', self)
        #self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))
        self.setWindowIcon(QIcon('./studyPyQt/movie.png'))

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
        url = self.tblResult.item(selected, 5).text()
        webbrowser.open(url) # 네이버 영화 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명을 입력하세요!')
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'movie' # movie로 변경하면 영화검색
        #    outputs = [] # 결과 담을 리스트변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # 테이블위젯에 출력 기능
            items = result['items'] # json결과 중  items 아래 배열만 추출
            self.makeTable(items)

    #테이블 위젯에 데이터표시 -- 네이버 영화 결과 변경
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일 선택
        self.tblResult.setColumnCount(7)
        self.tblResult.setRowCount(len(items)) # 현재 100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목','개봉년도','감독','배우진','평점','링크','포스터'])
        self.tblResult.setColumnWidth(0, 150)
        self.tblResult.setColumnWidth(1, 60) #개봉년도
        self.tblResult.setColumnWidth(4, 50) #평점

        # 컬럼 데이터를 수정금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 영화 ....
            # num = i + 1 # 뉴스번호
            title = self.replaceHtmlTag(post['title']) # HTMl 특수문자 변환 / 영어 제목 가져오기 추가
            subtitle = post['subtitle']
            title = f'{title} ({subtitle})'
            pubDate = post['pubDate']
            director = post['director'].replace('|',',')[:-1]
            actor = post['actor'].replace('|',',')[:-1] #[:-1] 파이썬에서만 가능!!
            userRating = post['userRating']
            link = post['link']
            
            img_url = post['image']

            #230308. 포스트 이미지 추가
            if img_url != '': # 빈값이 아니면 포스터가 있다.
                data = urlopen(img_url).read() # 2진데이터 - 네이버영화에 있는 이미지를 다운,텍스트형 데이터
                image = QImage() # 이미지 객체
                image.loadFromData(data)
                # QtableWidget 이미지를 그냥 넣을수 없음 QLabel() 집어넣은뒤 QLabel -> QTableWidget
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))

                # datafmf 이미지로 저장가능!
                # f = open(f'./studyPyQt/temp/image_{i+1}.png', mode='wb') #파일쓰기
                # f.write(data)
                # f.close()

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            #self.tblResult.setItem(i, 6, img_url)
            if img_url != '':
                self.tblResult.setCellWidget(i, 6, imgLabel)
                self.tblResult.setRowHeight(i, 110) # 포스터가 있으면 쉘 높이를 늘림
            else:
                self.tblResult.setItem(i, 6, QTableWidgetItem('No Poster!'))


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