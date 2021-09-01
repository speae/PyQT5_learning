## Ex 3-1. 창 띄우기

import sys
from PyQt5.QtWidgets import QApplication, QWidget


# MyApp 클래스는 QWidget으로부터 상속 -> QWidget이 가지는 함수를 동일하게 사용 가능
# 클래스를 상속받아서 내 클래스를 만드는 목적, 이유 -> QWidget 기능 + 내 기능 추가
class MyApp(QWidget):

    # 생성자
    def __init__(self):

        # super() -> 부모 클래스(QWidget)의 __init__()함수를 호출
        super().__init__()
        
        # MyApp 클래스 내부 함수 initUI를 실행
        self.initUI()

    # 생성 시 초기 설정 함수
    def initUI(self):
        
        # 윈도우 제목 설정
        self.setWindowTitle('My First Application')
        
        # 현재 모니터의 창이 뜰 때 초기 좌표(x, y) 설정
        self.move(1200, 300)
        
        # 윈도우의 크기
        self.resize(200, 200)

        # show()를 실행하지 않으면 위의 윈도우 특성 전용 X
        # 윈도우를 화면에 띄워줌
        self.show()


if __name__ == '__main__':

    # app 객체를 생성
    app = QApplication(sys.argv)

    # 우리가 구현하는 window 객체(MyApp)를 생성
    ex = MyApp()

    # 윈도우 객체 ex가 종료되기 전까지 sys.exit()를 호출X
    # 프로그램을 종료할 때 OS에게 정상 종료 여부 리턴
    sys.exit(app.exec_())
