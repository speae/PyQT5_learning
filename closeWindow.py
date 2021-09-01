## Ex 3-3. 창 닫기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication


class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      
      # 푸시 버튼 객체 생성
      btn = QPushButton('Quit', self)
      
      # 푸시 버튼 좌표를 설정
      btn.move(50, 50)
      
      # 푸시 버튼의 크기를 설정(텍스트 사이즈대로 resize)
      btn.resize(btn.sizeHint())

      # 시그널과 슬롯 등록(연결)
      # btn 버튼이 눌리면, QCoreApplication.instance().quit 함수를 호출
      btn.clicked.connect(QCoreApplication.instance().quit)

      self.setWindowTitle('Quit Button')
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())