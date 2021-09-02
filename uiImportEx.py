import sys

from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle as pkl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ui 파일을 가져오기 위한 패키지 임포트
from PyQt5 import uic, QtGui



# ui 파일을 읽어오기
form_class = uic.loadUiType("tool.ui")[0]


# 디스플레이 배율 및 레이아웃은 100%로 설정할 것
class MyApp(QWidget, form_class):

    def __init__(self):
        super().__init__()

        self.selectFile = ""
        self.img = None
        self.pixmap = []
        self.bboxes = np.array([])
        self.bboxes_ = np.array([])
        self.name_hflip = ""
        self.name_rotate = ""
        self.img_size = []
        self.result = np.array([])
        self.hflip_flag = False
        self.scale_flag = False
        self.trans_flag = False
        self.rotation_flag = False
        self.shearing_flag = False
        self.resizing_flag = False
        self.name = ""
        self.ext = ""

        self.setupUi(self)
        self.registerSignal()

    # 시그널과 슬롯을 등록
    def registerSignal(self):
        # print("register")

        # FileDialog에서 읽어온 파일명을 저장하는 변수
        self.btn_opendir.clicked.connect(self.showDialog)
        if self.img is None:
            self.showDialog()
        self.cb_hflip.stateChanged.connect(self.flag_hflip)
        self.cb_scaling.stateChanged.connect(self.flag_scale)
        self.cb_trans.stateChanged.connect(self.flag_trans)
        self.cb_rotation.stateChanged.connect(self.flag_rotation)
        self.cb_shearing.stateChanged.connect(self.flag_shearing)
        self.cb_resizing.stateChanged.connect(self.flag_resizing)

        # self.btn_preview.clicked.connect(self.process)

    def yolo2Libformat(self):
        # print("yolo2Libformat")

        self.img = cv2.imread(self.selectFile)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # jpg 확장자만 분리하여 txt파일 열기
        self.name, self.ext = os.path.splitext(self.selectFile)

        img_width = self.img.shape[1]
        img_height = self.img.shape[0]

        white_color = (255, 255, 255)

        # yolo v4포맷 파일 열기
        f = open(self.name + ".txt", 'r')
        if f is None:
            print('cannot open ' + self.name + '.txt')

        inner = []
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
            # print(x1, y1, x2, y2)

            inner.append([float(x1), float(y1), float(x2), float(y2), int(classNum)])

        f.close()

        # 바운딩 박스 데이터 저장
        self.bboxes = np.array(inner)

    def libformat2Yolo(self):
        # print("libformat2Yolo")

        f = open(self.name + ".txt", 'w')
        # print(self.name_hflip + ".txt")
        if f is None:
            print("Can't flip file open.")
            sys.exit()
        for value in self.bboxes_:
            x1, y1, x2, y2, classNum = value
            img_width = x2 - x1
            img_height = y2 - y1
            width_ratio = img_width / self.img_size[0]
            height_ratio = img_height / self.img_size[1]
            yolo_x1 = (x1 + img_width / 2) / self.img_size[0]
            yolo_y1 = (y1 + img_height / 2) / self.img_size[1]

            # print("img_width : {0}, img_height : {1}, width_ratio : {2}, height_ratio : {3}, yolo_x1 : {4}, "
            #       "yolo_y1 : {5}".format(img_width, img_height, width_ratio, height_ratio,
            #                              yolo_x1, yolo_y1))
            f.write(str(int(classNum)) + ' ' + str(round(yolo_x1, 4)) + ' ' + str(round(yolo_y1, 4)) + ' ' + str(
                round(width_ratio, 4)) + ' ' + str(round(height_ratio, 4)) + '\n')

        f.close()

    def process_hflip(self):
        # print("process_hflip")

        self.yolo2Libformat()

        # 이미지 좌우 대칭을 실행
        # 함수의 결과는 좌우 대칭된 이미지와 박스 좌표값을 리턴한다.
        img_, self.bboxes_ = RandomHorizontalFlip(1)(self.img.copy(), self.bboxes.copy())
        boxed_img = draw_rect(img_, self.bboxes_)
        HFlipImage = cv2.cvtColor(boxed_img, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_HFlip'
        cv2.imwrite(self.name + '.jpg', HFlipImage)

        self.img_size = (img_.shape[1], img_.shape[0])

        # 좌우 대칭 변환 이미지를 저장할 파일

        # 좌우 대칭 레이블 텍스트로 저장
        self.libformat2Yolo()

    def process_scale(self):
        self.yolo2Libformat()

        img_, bboxes_ = RandomScale(0.3, diff=True)(self.img.copy(), self.bboxes.copy())
        scaled_img = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_scale'
        cv2.imwrite(self.name + '.jpg', scaled_img)

        self.img_size = (img_.shape[1], img_.shape[0])
        self.libformat2Yolo()

    def process_trans(self):
        self.yolo2Libformat()

        img_, bboxes_ = RandomTranslate(0.3, diff=True)(self.img.copy(), self.bboxes.copy())
        translated_img = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_trans'
        cv2.imwrite(self.name + '.jpg', translated_img)

        self.img_size = (img_.shape[1], img_.shape[0])
        self.libformat2Yolo()

    def process_rotate(self):
        self.yolo2Libformat()

        img_, self.bboxes_ = RandomRotate(45)(self.img.copy(), self.bboxes.copy())
        rotated_img = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_rotate'
        cv2.imwrite(self.name + '.jpg', rotated_img)

        self.img_size = (img_.shape[1], img_.shape[0])
        self.libformat2Yolo()

    def process_shearing(self):
        self.yolo2Libformat()

        img_, self.bboxes_ = RandomShear(0.2)(self.img.copy(), self.bboxes.copy())
        rotated_img = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_shear'
        cv2.imwrite(self.name + '.jpg', rotated_img)

        self.img_size = (img_.shape[1], img_.shape[0])
        self.libformat2Yolo()

    def process_resizing(self):
        self.yolo2Libformat()

        img_, self.bboxes_ = Resize(600)(self.img.copy(), self.bboxes.copy())
        rotated_img = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)
        resize_img = cv2.resize(img_, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.result = resize_img
        self.bboxes = self.bboxes_

        self.imshow_result()

        # 좌우 대칭 이미지 저장
        self.name = self.name + '_resize'
        cv2.imwrite(self.name + '.jpg', rotated_img)

        self.img_size = (img_.shape[1], img_.shape[0])
        self.libformat2Yolo()

    def process(self):
        # print("process")
        # print(self.hflip_flag)

        if self.hflip_flag:
            # print("hflip process")
            self.process_hflip()
        elif not self.hflip_flag:
            # print("hflip process")
            self.imshow_org()

        if self.scale_flag:
            self.process_scale()
        elif not self.scale_flag:
            self.imshow_org()

        if self.trans_flag:
            self.process_trans()
        elif not self.trans_flag:
            self.imshow_org()

        if self.rotation_flag:
            self.process_rotate()
        elif not self.rotation_flag:
            self.imshow_org()

        if self.shearing_flag:
            self.process_shearing()
        elif not self.shearing_flag:
            self.imshow_org()

        if self.resizing_flag:
            self.process_resizing()
        elif not self.resizing_flag:
            self.imshow_org()

    # Qt.Checked = 2의 값을 가짐
    def flag_hflip(self, state):
        # print("flag_hflip")
        print(state)
        if state == Qt.Checked:
            self.hflip_flag = True
            self.process()
        else:
            self.hflip_flag = False
            self.process()

    def flag_scale(self, state):
        # print("flag_hflip")
        print(state)
        if state == Qt.Checked:
            self.scale_flag = True
            self.process()
        else:
            self.scale_flag = False
            self.process()

    def flag_trans(self, state):
        # print("flag_trans")
        if state == Qt.Checked:
            self.trans_flag = True
            self.process()
        else:
            self.trans_flag = False
            self.process()

    def flag_rotation(self, state):
        # print("flag_rotation")
        print(state)
        if state == Qt.Checked:
            self.rotation_flag = True
            self.process()
        else:
            self.rotation_flag = False
            self.process()

    def flag_shearing(self, state):
        # print("flag_shearing")
        if state == Qt.Checked:
            self.shearing_flag = True
            self.process()
        else:
            self.shearing_flag = False
            self.process()

    def flag_resizing(self, state):
        # print("flag_resizing")
        if state == Qt.Checked:
            self.resizing_flag = True
            self.process()
        else:
            self.resizing_flag = False
            self.process()

    def imshow_org(self):
        # print("imshow_org")
        self.pixmap = QPixmap(self.selectFile)
        self.lbl_org.setPixmap(self.pixmap.scaled(320, 240))

        if not self.hflip_flag and not self.scale_flag and not self.trans_flag and not self.rotation_flag \
                and not self.shearing_flag and not self.resizing_flag:
            self.lbl_result.setPixmap(self.pixmap.scaled(320, 240))

    def process_grey(self):
        # print("process_grey")
        self.img = cv2.imread(self.selectFile)
        if self.img is None:
            print(self.img, "isn't exist.")
            sys.exit()

        resize_img = cv2.resize(self.img, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        grey_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
        rgb_img = cv2.cvtColor(grey_img, cv2.COLOR_GRAY2RGB)

        h, w, c = rgb_img.shape
        qImg = QtGui.QImage(rgb_img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)

        self.lbl_result.setPixmap(pixmap)

        # cv2.imshow("test", rgb_img)

    # 경로 설정 시 한글 폴더 주의
    def showDialog(self):
        # print("showDialog")
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.selectFile = fname[0]
        self.lbl_debug.setText(fname[0])
        self.imshow_org()
        self.process_grey()

    def imshow_result(self):
        # print("imshow_result")
        h, w, c = self.result.shape
        qImg = QtGui.QImage(self.result.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.lbl_result.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
