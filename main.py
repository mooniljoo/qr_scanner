# -*- coding:utf-8 -*-

import sys

import matplotlib.pyplot as plt
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import re

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

mainUI = 'ui/main.ui'


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(mainUI, self)

        self.btn_upload.clicked.connect(self.open_file)

    def show_image_in_display(self, image_path):
        self.input_img.setPixmap(QPixmap(image_path))

    def show_value_in_display(self, img):
        bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(bw)

        if decoded:
            for d in decoded:
                self.label_2.setText(d.type)
                self.label_4.setText(d.data.decode('utf-8'))
                print(d.type)
                print(d.data.decode('utf-8'))

                cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] +
                                                            d.rect[2], d.rect[1]+d.rect[3]), (0, 0, 255), 2)

        else:
            self.label_2.setText('')
            self.label_4.setText('코드인식에 실패하였습니다.')

    def open_file(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "불러올 이미지를 선택하세요.", "", "All Files (*);;Python Files (*.py)")

        if filePath:
            print(filePath)
            self.show_image_in_display(filePath)

            if re.compile('[^ㄱ-ㅣ가-힣]+').sub('', filePath):
                # 한글 처리
                stream = open(filePath.encode("utf-8"), "rb")
                bytes = bytearray(stream.read())
                numpyArray = np.asarray(bytes, dtype=np.uint8)

                img = cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
                self.show_value_in_display(img)

            else:
                img = cv2.imread(filePath)
                self.show_value_in_display(img)


app = QApplication([])
# app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
