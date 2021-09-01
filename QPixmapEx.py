## Ex 5-12. QPixmap.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 이미지 파일을 읽어서 pixmap
        pixmap = QPixmap('img/background.jpg')

        # label 객체 선언
        lbl_img = QLabel()
        
        # pixmap이 불러온 이미지를 lbl_img에 출력하게 설정
        lbl_img.setPixmap(pixmap)
        
        # pixmap은 단순히 이미지만 가지고 있는게 아니라, 이미지 정보(메타데이터 : 이미지 크기, 포맷)
        lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        lbl_size.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_size)
        self.setLayout(vbox)

        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())