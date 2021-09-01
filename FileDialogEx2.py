## Ex 5-1. QPushButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QAction, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Push Button을 객체 생성하면서 버튼 위에 표시되는 문자열 지정; 단축키와 함께 '&'는 단축키 지정
        # & + alphabet : 단축키 설정

        # alt + b
        btn1 = QPushButton('Open', self)
        btn1.setIcon(QIcon("icons/open.png"))
        btn1.setIconSize(QSize(48, 48))

        # 버튼이 눌려있는 상태 시작 여부
        # btn1.setCheckable(True)
        # btn1.setCheckable(False)

        # 한번씩 눌릴때마다 상태 반전; True<->False
        # btn1.toggle()

        # alt + 2
        # btn2 = QPushButton('Button&2', self)
        # btn2 = QPushButton(self)
        # btn2.setText('Button&2')

        btn2 = QPushButton('Open Dir', self)
        btn2.setIcon(QIcon("icons/open.png"))
        btn2.clicked.connect(self.showDialog)

        # openDir = QAction(QIcon('open.png'), 'Open', self)
        # openDir.setShortcut('Ctrl+O')
        # openDir.setStatusTip('Open Dir')
        # openDir.triggered.connect(self.showDialog)

        # 버튼 비활성화 상태
        # btn3 = QPushButton('Button3', self)
        # btn3.setEnabled(False)

        btn3 = QPushButton('Change Save Dir', self)
        btn3.setIcon(QIcon("icons/open.png"))

        pixmap = QPixmap('img/background.jpg')

        # self를 앞에 븉여주어 MyApp 클래스의 어느 위치(함수)에서든 접근 가능
        # 클래스 안에서 사용할 수 있는 전역변수로 선언
        # self.imgLabel = QLabel('', self)
        # self.imgLabel.setAlignment(Qt.AlignVCenter)
        self.imgLabel = QLabel()
        self.imgLabel.setPixmap(pixmap.scaled(640, 480))

        # self.imgInfoLabel = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        # self.imgInfoLabel.setAlignment(Qt.AlignCenter)

        # Vertical Box Layout
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        # vbox.addItem(openDir)
        vbox.addWidget(btn3)

        # Horizontal Box Layout
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.imgLabel)

        self.setLayout(vbox)
        self.setLayout(hbox)
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(fname[0])

        if fname[0]:
            # f = open(fname[0], 'r')
            self.imgLabel.setText(fname[0])

            # with f:
            #     data = f.read()
            #     self.imgLabel.setText(data)


if __name__ == '__main__':

    # int main(argc, argv : 문자열(배열))
    # 마우스 클릭, 키보드 등 사용자 인터페이스를 이벤트 루프에서 받아들여 QApplication() 메소드에서 처리하여
    # 어떤 callback 함수가 있는 슬롯에서 호출
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
