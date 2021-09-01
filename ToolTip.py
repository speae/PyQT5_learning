## Ex 3-4. 툴팁 나타내기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QFont


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 폰트를 불러와서, 툴팁에서 사용할 폰트 설정, 글자 크기
        QToolTip.setFont(QFont('SansSerif', 10))
        
        # 툴팁에 띄울 메시지
        # 창 안에 마우스 포인터를 올렸을 때 뜨는 메시지
        # self는 윈도우를 가리키는 지시자
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        
        # 버튼 위에 마우스 포인터를 올렸을 때
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())

        self.setWindowTitle('Tooltips')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())