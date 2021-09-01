## Ex 3-6. 메뉴바 만들기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 아이콘 등록
        exitAction = QAction(QIcon('img/exit.png'), 'Exit', self)
        
        # 단축키 등록
        exitAction.setShortcut('Ctrl+Q')
        
        # 툴팁 등록
        exitAction.setStatusTip('Exit application')
        
        # 이벤트 발생 시 qApp.quit 호출 -> 종료
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())