from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
import time

class interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Korea Sign Lanuage Recognater")
        self.setGeometry(150,150, 900, 900)
        self.initUI()
    
    def initUI(self):
        self.cpt = cv2.VideoCapture(0)
        self.fps = 30
        self.sens = 300
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        cv2.imwrite("img_0.jpg", self.img_o)

        self.cnt = 0

        self.frame = QLabel(self)
        self.frame.resize(890, 600)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)

        self.btn_on = QPushButton("시작", self)
        self.btn_on.resize(100, 25)
        self.btn_on.move(5,610)
        self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("종료", self)
        self.btn_off.resize(100, 25)
        self.btn_off.move(5+100+5,610)
        self.btn_off.clicked.connect(self.stop)

        self.prt = QLabel(self)
        self.prt.resize(200, 25)
        self.prt.move(5+105+105, 610)

        self.fps_slider = QSlider(Qt.Horizontal, self)
        self.fps_slider.resize(100, 25)
        self.fps_slider.move(5+105+105+200, 610)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(30)
        self.fps_slider.setValue(30)
        self.fps_slider.valueChanged.connect(self.setFPS)
        self.fps_slider.sliderReleased.connect(self.notiFPS)

        self.sens_slider = QSlider(Qt.Horizontal, self)
        self.sens_slider.resize(100, 25)
        self.sens_slider.move(5+105+105+200+105,610)
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

        self.show()
    

    def setFPS(self):
        self.fps = self.fps_slider.value()
        try:
            self.timer.stop()
            self.timer.start(1000. / self.fps)
        except:
            pass
        self.prt.setText("FPS :" + str(self.fps))

    def setSens(self):
        self.sens = self.sens_slider.value()
        self.prt.setText("Sens: " + str(self.sens))

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000. / self.fps)
        self.txtNoti.append("Log     | Camera Start")

    def notiFPS(self): 
        self.fps = self.fps_slider.value()
        try:
            self.timer.stop()
            self.timer.start(1000. / self.fps)
        except:
            pass    
        self.txtNoti.append("Log     | Chage FPS to " + str(self.fps))
        
    
    def notiSens(self):
        self.sens = self.sens_slider.value()
        self.txtNoti.append("Log     | Chage Sens to " + str(self.sens))

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
        self.frame.setPixmap(QPixmap.fromImage(QImage()))
        self.timer.stop()
        self.txtNoti.append("Log     | Camera Stop")

    def compare(self, img_o, img_p):
        err = np.sum((img_o.astype("float") - img_p.astype("float")) ** 2)
        err /= float(img_o.shape[0] * img_p.shape[1])
        if(err >= self.sens):
            t = time.localtime()
            self.prt.setText("{}-{}-{} {}:{}:{} 움직임 감지".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))

app= QApplication(sys.argv)
w = interface()
sys.exit(app.exec_())
