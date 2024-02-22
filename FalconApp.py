import random
import time

import cv2
import numpy as np
import torch
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPainterPath, QImage
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QGraphicsScene, \
    QGraphicsEllipseItem, QGraphicsView, QGraphicsProxyWidget, QGraphicsTextItem
from PyQt5.QtCore import Qt, QFile,QLocale
from PyQt5 import QtCore
import matplotlib

from GenderClassification.app import Model

matplotlib.use('Qt5Agg')
from PyQt5.QtGui import QColor
import pyqtgraph as pg

import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = loadUi(r"C:\Users\PC\PycharmProjects\pythonProject2\GenderClassification\app\appui.ui", self)

        self.start_time = time.time()
        self.start_date = time.strftime("%H:%M")
        self.yesterday_male_count = []
        self.yesterday_female_count = []
        self.yesterday_customer_count = []

        self.this_mounth_male_count = []
        self.this_mounth_female_count = []
        self.this_mounth_customer_count = []

        self.this_year_male_count = []
        self.this_year_female_count = []
        self.this_year_customer_count = []

        self.hours = [0]
        self.customer = [0]

        self.run_time = self.findChild(QLabel, "label_run_time")
        self.total_customer_count_label = self.findChild(QLabel, "label_total_customer2")
        self.label_status = self.findChild(QLabel, "label_status")
        self.camera_customer_count = 0
        self.current_count = 0
        self.start = False

        self.cam = cv2.VideoCapture(r"C:\Users\PC\Desktop\DatasetVideos\0000.mp4")
        self.model = Model.ObjectDetection(torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True))
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.update_camera_stats)
        self.timer.start()
        self.total_visits = self.findChild(QLabel, "label_total_visits")
        self.started_at_label = self.findChild(QLabel, "started_at")






        self.cap = cv2.VideoCapture(r"C:\Users\PC\Desktop\DatasetVideos\11.mp4")

        self.home_page()


        self.statistics_page()


        self.show_page(0)
        self.update_camera()



    def show_page(self, index):
        if index == 0:
            self.ui.pushButton_1.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color:  rgb(161, 161, 161);
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        else:
            self.ui.pushButton_1.setStyleSheet(('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color: white;
            border-radius: 10px;
            padding: 10px;
            text-align: left}'''))
        if index == 1:
            self.ui.pushButton_2.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color:  rgb(161, 161, 161);
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        else:
            self.ui.pushButton_2.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color: white;
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')

        if index == 2:
            self.ui.pushButton_3.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color:  rgb(161, 161, 161);
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        else:
            self.ui.pushButton_3.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color: white;
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        if index == 3:
            self.ui.pushButton_4.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color:  rgb(161, 161, 161);
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        else:
            self.ui.pushButton_4.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color: white;
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        if index == 4:
            self.ui.pushButton_5.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color:  rgb(161, 161, 161);
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')
        else:
            self.ui.pushButton_5.setStyleSheet('''QPushButton {
	        font: 10pt "Segoe UI Emoji";
	        background-color: white;
            border-radius: 10px;
            padding: 10px;
            text-align: left}''')

        self.ui.stackedWidget.setCurrentIndex(index)

    def displayTime(self):
        local = QLocale(QLocale.English)
        time = QtCore.QDateTime.currentDateTime().toString("hh:mm")
        day = local.toString(QtCore.QDateTime.currentDateTime(),"dddd")
        self.label_time = self.findChild(QLabel, "label_time")
        self.label_day = self.findChild(QLabel, "label_day")
        self.label_time.setText(time)
        self.label_day.setText(day)

    def home_page(self):
        local = QLocale(QLocale.English)
        self.label_time = self.findChild(QLabel, "label_time")
        self.label_day = self.findChild(QLabel, "label_day")
        self.label_average_age = self.findChild(QLabel, "label_avg_age")
        self.avg_male_count = self.findChild(QLabel, "label_avg_male")
        self.avg_female_count = self.findChild(QLabel, "label_avg_female")
        self.total_male_count = self.findChild(QLabel, "label_total_male")
        self.total_female_count = self.findChild(QLabel, "label_total_female")
        self.total_customer_count = self.findChild(QLabel, "label_total_customer")




        time = QtCore.QDateTime.currentDateTime().toString("hh:mm")
        day = local.toString(QtCore.QDateTime.currentDateTime(), "dddd")
        self.label_time.setText(time)
        self.label_day.setText(day)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start()

        self.ui.pushButton_1.clicked.connect(lambda: self.show_page(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.show_page(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.show_page(2))
        self.ui.pushButton_4.clicked.connect(lambda: self.show_page(3))
        self.ui.pushButton_5.clicked.connect(lambda: self.show_page(4))



    def update_graph(self):
        self.customer.append(int(self.camera_customer_count))
        self.hours.append(max(self.hours) + 0.00083333333)
        pen = pg.mkPen(color=(0, 128, 255), width=1, cosmetic=True)
        plot_widget = pg.PlotWidget()
        plot_widget.plot(self.hours, self.customer, pen=pen, symbolPen=None, symbolSize=1,
                         symbolBrush=(0, 255, 255))

        plot_widget.setFixedWidth(500)
        plot_widget.setFixedHeight(270)
        plot_widget.setXRange(0, max(self.customer)+ 50)
        plot_widget.setYRange(0, max(self.hours) + 7)
        plot_widget.setBackground("white")

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(plot_widget)
        self.scene.addItem(proxy_widget)


    def camera_page(self):
        if self.start == True:

          label = self.findChild(QLabel, "label_3")
          ret, frame = self.cap.read()

          start_time = time.time()
          processed_frame, self.camera_customer_count, self.current_count, new_detected = self.model.__call__(frame)
          end_time = time.time()

          height, width, channel = processed_frame.shape

          bytes_per_line = 3 * width
          q_image = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
          pixmap = QPixmap.fromImage(q_image)


          label.setPixmap(pixmap)


          label.setScaledContents(True)


          fps = 1 / np.round(end_time - start_time, 3)
          print(fps)


    def update_camera(self):
        self.ui.pushButton.clicked.connect(lambda: self.start_stop())
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(75)
        self.timer.timeout.connect(self.camera_page)
        self.timer.start()
    def update_camera_stats(self):
        current_time = time.time()
        run_time =  int(np.round(current_time - self.start_time, 0) / 60)
        run_time_label = self.findChild(QLabel, "label_run_time")
        total_person_count = self.findChild(QLabel, "label_total_customer2")
        current_detected =  self.findChild(QLabel, "currentcount")
        current_detected.setText(str(self.current_count))
        run_time_label.setText(str(run_time) + " Min.")
        total_person_count.setText(str(self.camera_customer_count))
        self.total_visits.setText(str(self.camera_customer_count))
        self.started_at_label.setText(str(self.start_date))
    def start_stop(self):
        print(self.start)
        if self.start == False:
             self.ui.pushButton.setText("STOP")
             self.label_status.setText("Running")
             self.label_status.setStyleSheet("color: rgb(0, 255, 0);font: 25pt 'Segoe UI Emoji';")
             self.ui.pushButton.setStyleSheet('color: rgb(255, 0, 0);background-color: rgb(0, 0, 0);font: 87 48pt "Segoe UI Black";')
             self.start = True
        elif self.start == True:
            self.ui.pushButton.setText("START")
            self.label_status.setText("Stopped")
            self.label_status.setStyleSheet("color: rgb(255,0 , 0);font: 25pt 'Segoe UI Emoji';")
            self.ui.pushButton.setStyleSheet('color: rgb(0, 255, 0);background-color: rgb(0, 0, 0);font: 87 48pt "Segoe UI Black";')
            self.start = False









    def statistics_page(self):

        plot_widget1 = pg.PlotWidget()
        plot_widget2 = pg.PlotWidget()
        plot_widget3 = pg.PlotWidget()
        plot_widget4 = pg.PlotWidget()

        pen1 = pg.mkPen(color=(0, 128, 255), width=1, cosmetic=True)
        pen2 = pg.mkPen(color=(255, 37, 121), width=1, cosmetic=True)
        pen3 = pg.mkPen(color=(0, 255, 0), width=1, cosmetic=True)


        bar1 = pg.BarGraphItem(x=[1], height=[5], width=0.05, brush=QColor(255, 37, 121))
        bar2 = pg.BarGraphItem(x=[1.07], height=[10], width=0.05, brush=QColor(0, 128, 255))
        x_axis = pg.AxisItem(orientation='bottom')
        x_axis.setTicks([[(1, 'Male'), (1.07, 'Female')]])
        plot_widget1.setAxisItems({'bottom': x_axis})





        plot_widget1.addItem(bar1)
        plot_widget1.addItem(bar2)



        plot_widget2.plot([1, 2, 3, 4, 5, 6, 7], [2, 3, 3, 3, 6, 4, 5], pen=pen1, symbolPen=None, symbolSize=10,
                          symbolBrush=(0, 128, 255))
        plot_widget2.plot([1, 2, 3, 4, 5, 6, 7], [2, 4, 5, 4, 4, 3, 4], pen=pen2, symbolPen=None, symbolSize=10,
                          symbolBrush=(255, 37, 121))


        plot_widget3.plot([1, 2, 3, 4, 5, 6, 7], [2, 3, 3, 3, 6, 4, 5], pen=pen1, symbolPen=None, symbolSize=10,
                          symbolBrush=(0, 128, 255))
        plot_widget3.plot([1, 2, 3, 4, 5, 6, 7], [2, 4, 5, 4, 4, 3, 4], pen=pen2, symbolPen=None, symbolSize=10,
                          symbolBrush=(255, 37, 121))


        plot_widget4.plot([1, 2, 3, 4, 5, 6, 7], [2, 3, 3, 3, 6, 4, 5], pen=pen1, symbolPen=None, symbolSize=10,
                          symbolBrush=(0, 128, 255))
        plot_widget4.plot([1, 2, 3, 4, 5, 6, 7], [2, 4, 5, 4, 4, 3, 4], pen=pen2, symbolPen=None, symbolSize=10,
                          symbolBrush=(255, 37, 121))

        plot_widget1.setFixedWidth(350)
        plot_widget1.setFixedHeight(200)
        plot_widget1.setBackground("white")


        plot_widget2.setFixedWidth(400)
        plot_widget2.setFixedHeight(230)
        plot_widget2.setBackground("white")


        plot_widget3.setFixedWidth(410)
        plot_widget3.setFixedHeight(230)
        plot_widget3.setBackground("white")


        plot_widget4.setFixedWidth(410)
        plot_widget4.setFixedHeight(230)
        plot_widget4.setBackground("white")



        scene1 = QGraphicsScene()
        scene2 = QGraphicsScene()
        scene3 = QGraphicsScene()
        scene4 = QGraphicsScene()

        self.ui.graphicsView_2.setScene(scene1)
        self.ui.graphicsView_3.setScene(scene2)
        self.ui.graphicsView_4.setScene(scene3)
        self.ui.graphicsView_5.setScene(scene4)

        proxy_widget1 = QGraphicsProxyWidget()
        proxy_widget2 = QGraphicsProxyWidget()
        proxy_widget3 = QGraphicsProxyWidget()
        proxy_widget4 = QGraphicsProxyWidget()

        proxy_widget1.setWidget(plot_widget1)
        proxy_widget2.setWidget(plot_widget2)
        proxy_widget3.setWidget(plot_widget3)
        proxy_widget4.setWidget(plot_widget4)

        scene1.addItem(proxy_widget1)
        scene2.addItem(proxy_widget2)
        scene3.addItem(proxy_widget3)
        scene4.addItem(proxy_widget4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

