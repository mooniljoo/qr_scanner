# -*- coding:utf-8 -*-

import sys

import matplotlib.pyplot as plt
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import os
import re
import glob
import clipboard

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

mainUI = 'ui/main2.ui'


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(mainUI, self)

        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_upload_folder.clicked.connect(self.upload_folder)
        self.btn_copy.clicked.connect(self.copy_result_value)
        self.list_folder.itemClicked.connect(self.click_item_in_list)

        # init
        self.dirPath = ''

    def get_file_size(self, filePath):
        try:
            n = os.path.getsize(filePath)
            b = "%.2f Bytes" % n
            kb = "%.2f KB" % (n / 1024)
            mb = "%.2f MB" % (n / (1024.0 * 1024.0))
            self.lbl_size.setText(kb)
        except os.error:
            print("파일이 없거나 에러입니다.")

    def copy_result_value(self):
        clipboard.copy(self.label_4.toPlainText())
        print("Result Values are Copied!")

    def show_image_in_display(self, image_path):
        self.input_img.setPixmap(QPixmap(image_path))

    def show_value_in_display(self, img):
        if img is not None:
            bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            decoded = pyzbar.decode(bw)

            if decoded:
                for d in decoded:
                    codeType = self.label_2.setText(d.type)
                    codeValue = d.data.decode('utf-8')
                    print(codeValue)

                    self.label_4.clear()
                    self.label_4.setText(
                        "<span>"+codeValue+"</span>")

                    if codeValue.find('http') == 0:
                        url = codeValue

                        self.label_4.setText(
                            "<a href="+url+">"+url+"</a>")

            else:
                self.label_2.setText('')
                self.label_4.setText(
                    "<span>코드인식에 실패하였습니다.</span>")
                # self.label_4.setPlainText('코드인식에 실패하였습니다.')
        else:
            QMessageBox.information(self, "파일 종류 오류", "이미지파일이 아닙니다.")

    def list_files_in_folder(self, dirPath):
        file_list = glob.glob(dirPath + '/*.*')

        self.list_folder.clear()
        for f in file_list:
            fname = f.split('\\')[1]
            # print(fname)
            self.list_folder.addItem(fname)

    def classify_filePath(self, filePath):
        if filePath:
            # print(filePath)
            self.show_image_in_display(filePath)
            self.get_file_size(filePath)

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

    def click_item_in_list(self, item):
        # print(self.dirPath + '/'+item.text())

        self.classify_filePath(self.dirPath + '/'+item.text())
        # QMessageBox.information(self, "ListWidget", item.text())

    def open_file(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "불러올 이미지를 선택하세요.", "", "All Files (*);;Python Files (*.py)")

        self.classify_filePath(filePath)

    def upload_folder(self):
        dirPath = QFileDialog.getExistingDirectory(
            self, "목록에 올릴 폴더를 선택하세요.")
        if dirPath:
            self.list_files_in_folder(dirPath)
            self.dirPath = dirPath


app = QApplication([])
# app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
