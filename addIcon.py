## Ex 3-2. 어플리케이션 아이콘 넣기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class MyApp(QWidget):

  def __init__(self):

      # 부모 클래스의 __init()__함수 호출
      super().__init__()
      self.initUI()

  def initUI(self):
      self.setWindowTitle('Icon')
      
      # QICon으로 이미지를 불러와서 아이콘 설정하기
      self.setWindowIcon(QIcon('img/web.png'))
      
      # 창을 특정 좌표에 띄워주고 창 사이즈도 설정
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())