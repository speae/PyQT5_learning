import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

# ui파일을 가져오기 위한 패키지 임포트
from PyQt5 import uic, QtGui

# ui파일을 읽어오기
form_class = uic.loadUiType("tool.ui")[0]

class MyApp(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registerSignal()

    # 시그널과 슬롯을 등록한다.
    def registerSignal(self):
        # FileDialog에서 읽어온 파일명을 저장하는 변수
        self.selectFile = ""
        self.btn_opendir.clicked.connect(self.showDialog)
        self.cb_hflip.stateChanged.connect(self.flag_hflip)
        self.cb_trans.stateChanged.connect(self.flag_trans)
        self.cb_rotation.stateChanged.connect(self.flag_rotation)
        self.cb_shearing.stateChanged.connect(self.flag_shearing)
        self.cb_resizing.stateChanged.connect(self.flag_resizing)
        self.btn_preview.clicked.connect(self.process)

    def process(self):
        if self.hflag == True:
            self.process_hflip()


    def flag_hflip(self, state):
        if state == Qt.Checked: self.hflag = True
        else:                   self.hflag = False

    def flag_trans(self, state):
        if state == Qt.Checked: self.trans_flag = True
        else:                   self.trans_flag = False

    def flag_rotation(self, state):
        if state == Qt.Checked: self.rotation_flag = True
        else:                   self.rotation_flag = False

    def flag_shearing(self, state):
        if state == Qt.Checked: self.shearing_flag = True
        else:                   self.shearing_flag = False

    def flag_resizing(self, state):
        if state == Qt.Checked: self.resizing_flag = True
        else:                   self.resizing_flag = False


    def process_hflip(self):

        self.yolo2Libformat()
        # 이미지 좌우 대칭을 실행
        # 함수의 결과는 좌우 대칭된 이미지와 박스 좌표값을 리턴한다.
        img_, bboxes_ = RandomHorizontalFlip(1)(self.img.copy(), self.bboxes.copy())
        HFlipImage = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.imshow_result()

        # 좌우 대칭 변환 이미지를 저장할 파일명
        name_hflip = self.name + '_HFlip'
        # 좌우 대칭 이미지 저장
        cv2.imwrite(name_hflip + '.jpg', HFlipImage)

        img_size = (img_.shape[1], img_.shape[0])
        # 좌우 대칭 레이블 텍스트로 저장
        self.libformat2Yolo(bboxes_, img_size, name_hflip)

        # plotted_img = draw_rect(img_, bboxes_)
        # plt.imshow(plotted_img)
        # plt.show()


    def yolo2Libformat(self):
        inner = []
        self.img = cv2.imread(self.selectFile)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        img_width = self.img.shape[1]
        img_height = self.img.shape[0]

        white_color = (255, 255, 255)

        # jpg 확장자만 분리하여 txt파일 열기
        self.name, ext = os.path.splitext(self.selectFile)

        # yolo v4포맷 파일 열기
        try:
            f = open(self.name + ".txt", 'r')
        except OSError:
            print('cannot open ' + self.name + '.txt')

        while True:
            # 문자열 한줄을 읽어와서
            line = f.readline()

            # 문자열이 비어있다면 종료
            if not line:
                break

            # 문자열이 비어있지 않으면 문자열 나눠서 디코딩
            classNum, x, y, width_ratio, height_ratio = line.split(' ')
            # 박스의 센터 좌표값
            x_pos = round(img_width * float(x))
            y_pos = round(img_height * float(y))
            width_pixel = round(img_width * float(width_ratio))
            height_pixel = round(img_height * float(height_ratio))
            x1 = round(x_pos - width_pixel / 2)
            y1 = round(y_pos - height_pixel / 2)
            x2 = round(x_pos + width_pixel / 2)
            y2 = round(y_pos + height_pixel / 2)

            # img = cv2.rectangle(img, (x1,y1), (x2,y2), white_color, 3)
            print(x1, y1, x2, y2)

            inner.append([float(x1), float(y1), float(x2), float(y2), int(classNum)])

        f.close()
        self.bboxes = np.array(inner)




    def libformat2Yolo(self, bboxes, image_size, name):
        f = open(name + '.txt', 'w')

        for value in bboxes:
            x1, y1, x2, y2, classNum = value
            img_width = x2 - x1
            img_height = y2 - y1
            width_ratio = img_width / image_size[0]
            height_ratio = img_height / image_size[1]
            yolo_x1 = (x1 + img_width / 2) / image_size[0]
            yolo_y1 = (y1 + img_height / 2) / image_size[1]
            f.write(str(int(classNum)) + ' ' + str(round(yolo_x1, 4)) + ' ' + str(round(yolo_y1, 4)) + ' ' + str(
                round(width_ratio, 4)) + ' ' + str(round(height_ratio, 4)) + '\n')

        f.close()


    # 경로 설정시 한글 폴더명은 이슈 있음
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.selectFile = fname[0]
        self.lbl_debug.setText(fname[0])
        self.imshow_org()
        #self.process_grey()

    def imshow_org(self):
        self.pixmap = QPixmap(self.selectFile)
        self.lbl_org.setPixmap(self.pixmap.scaled(320,240))

    def imshow_result(self):
        h, w, c = self.result.shape
        qImg = QtGui.QImage(self.result.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.lbl_result.setPixmap(pixmap)


        self.lbl_org.setPixmap(self.pixmap.scaled(320,240))


    def process_grey(self):
        img = cv2.imread(self.selectFile)
        resize_img = cv2.resize(img, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        grey_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
        rgb_img = cv2.cvtColor(grey_img, cv2.COLOR_GRAY2RGB)

        h, w, c = rgb_img.shape
        qImg = QtGui.QImage(rgb_img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.lbl_result.setPixmap(pixmap)

        #cv2.imshow("test", rgb_img)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())