from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
import time

class interface(QWidget):
    videoFlag = False
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Korea Sign Lanuage Recognater")
        self.setGeometry(150,150, 900, 900)
        self.initUI()
    
    def initUI(self):
        self.cpt = cv2.VideoCapture(0)
        self.fps = 30
        self.sens = 500
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        cv2.imwrite("img_0.jpg", self.img_o)

        self.cnt = 0

        self.frame = QLabel(self)
        self.frame.resize(890, 570)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)

        self.btn_on = QPushButton("시작", self)
        self.btn_on.resize(100, 25)
        self.btn_on.move(5,590)
        self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("종료", self)
        self.btn_off.resize(100, 25)
        self.btn_off.move(5+100+5,590)
        self.btn_off.clicked.connect(self.stop)

        self.prt = QLabel(self)
        self.prt.resize(200, 25)
        self.prt.move(5+105+105, 593)

        self.lblfps = QLabel(self)
        self.lblfps.resize(200, 25)
        self.lblfps.move(460 + 93, 580)
        self.lblfps.setText("FPS Control")
        self.fps_slider = QSlider(Qt.Horizontal, self)
        self.fps_slider.resize(100, 25)
        self.fps_slider.move(450 + 90, 610)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(30)
        self.fps_slider.setValue(30)
        self.fps_slider.valueChanged.connect(self.setFPS)
        self.fps_slider.sliderReleased.connect(self.notiFPS)

        self.lblSens = QLabel(self)
        self.lblSens.resize(200, 25)
        self.lblSens.move(710, 580)
        self.lblSens.setText("Sens Control")
        self.sens_slider = QSlider(Qt.Horizontal, self)
        self.sens_slider.resize(100, 25)
        self.sens_slider.move(700,610)
        self.sens_slider.setMinimum(50)
        self.sens_slider.setMaximum(500)
        self.sens_slider.setValue(300)
        self.sens_slider.valueChanged.connect(self.setSens)
        self.sens_slider.sliderReleased.connect(self.notiSens)
        
        self.lblRecog = QLabel(self)
        self.lblRecog.setText("인식 값")
        self.lblRecog.resize(100, 25)
        self.lblRecog.setScaledContents(True)
        self.lblRecog.move(200,640)

        self.lblNoti = QLabel(self)
        self.lblNoti.setText("공지사항/로그")
        self.lblNoti.resize(100, 25)
        self.lblNoti.setScaledContents(True)
        self.lblNoti.move(635,640)

        self.txtRecog = QTextBrowser(self)
        self.txtRecog.resize(440, 110)
        self.txtRecog.move(5, 670)

        self.txtNoti = QTextBrowser(self)
        self.txtNoti.resize(440, 110)
        self.txtNoti.move(455, 670)
        self.txtNoti.append("Notify | 1. you can chage FPS using FPS Control")
        self.txtNoti.append("Notify | 2. you can chage Sensitivity using Sens Control")
        self.txtNoti.append("Notify | 3. you can turn on WebCam to click Start Button")
        self.txtNoti.append("Notify | 4. you can turn off WebCam to click End Button")
        self.txtNoti.append("Notify | 5. If program recoginze sign lanuage, ")
        self.txtNoti.append("Notify |    print class in txt-Recoginze")

        
        self.show()
    
    def setFPS(self):
        self.fps = self.fps_slider.value()
        try:
            self.timer.stop()
            self.timer.start(1000. / self.fps)
        except:
            self.frame.setPixmap(QPixmap.fromImage(QImage()))
            pass
        t = time.localtime()
        self.prt.setText("FPS :" + str(self.fps)+ " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))

    def setSens(self):
        self.sens = self.sens_slider.value()
        t = time.localtime()
        self.prt.setText("Sens: " + str(self.sens) + " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))

    def notiFPS(self): 
        self.fps = self.fps_slider.value()
        try:
            self.timer.stop()
            self.timer.start(1000. / self.fps)
        except:
            pass
        t = time.localtime()
        self.txtNoti.append("Log     | Chage FPS to " + str(self.fps) + " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))
        
    def notiSens(self):
        self.sens = self.sens_slider.value()
        t = time.localtime()
        self.txtNoti.append("Log     | Chage Sens to " + str(self.sens) + " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))

    def start(self):
        t = time.localtime()
        if self.videoFlag == True:
            self.txtNoti.append("Notify | Camera is alrady start | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))
        else:
            self.videoFlag = True
            self.timer = QTimer()
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(1000. / self.fps)
            self.txtNoti.append("Log     | Camera Start" + " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        
        self.img_p = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("img_p.jpg", self.img_p)
        self.compare(self.img_o, self.img_p)
        self.img_o = self.img_p.copy()
        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix) 

    def stop(self):
        t = time.localtime()
        if self.videoFlag == False:
            self.txtNoti.append("Notify | Camera is alrady start | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))
        else:
            self.videoFlag = False
            self.frame.setPixmap(QPixmap.fromImage(QImage()))
            self.timer.stop()
            self.txtNoti.append("Log     | Camera Stop" + " | {}:{}:{}".format(t.tm_hour, t.tm_min, t.tm_sec))

    def compare(self, img_o, img_p):
        err = np.sum((img_o.astype("float") - img_p.astype("float")) ** 2)
        err /= float(img_o.shape[0] * img_p.shape[1])
        if(err >= self.sens):
            t = time.localtime()
            self.prt.setText("{}-{}-{} {}:{}:{} 움직임 감지".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))

app= QApplication(sys.argv)
w = interface()
sys.exit(app.exec_())
