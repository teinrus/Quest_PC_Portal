import json
import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets

import RPi.GPIO as GPIO

# define constant GPIO name

IN_START = 27
IN_STARTPOZNAVATVIDEO = 22 #позновательное видео в цикле
IN_STARTSOBRANIEVIDEO = 18 #видео 1 раз собрание директоров
IN_ARDSTARTVIDEO = 23 #видео 7 секунд логотип
IN_ARDSTOPVIDEO = 24 #видео без звука 

 
DATA_DIRNAME = 'media'
LOGO_FILENAME = 'logo.jpg'
FILENAME  = '0001.mp4'
FILENAME1 = '1111.mp4'
FILENAME2 = '2222.mp4'
FILENAME3 = '3333.mp4'

class IOThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self, handler):
        super().__init__()
        self.signal.connect(handler)
        self.running = True
        self.loop = False
        self.playing = False

    def run(self):
        import random
        while self.running:
            if GPIO.input(IN_STARTPOZNAVATVIDEO) == True:
                if not self.playing == True:
                    self.playing =True 
                    self.signal.emit(1)
                    self.loop=True
            elif self.playing ==True:
                self.playing=False
                self.loop = False
                self.signal.emit(5) 

            if GPIO.input(IN_STARTSOBRANIEVIDEO) == True:
                self.signal.emit(2)
            if GPIO.input(IN_ARDLOGOVIDEO) == True:
                self.signal.emit(3)
            if GPIO.input(IN_ARDSTARTVIDEO) == True:
                self.signal.emit(4)
            if GPIO.input(IN_ARDSTOPVIDEO) == True:
                self.signal.emit(5) 
            self.sleep(1)

    def stop(self):
        self.running = False
        self.wait()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.loop = False
        self.sourceFileName =''
        self.setMinimumSize(QtCore.QSize(800, 640))  
        self.setWindowTitle('Просмотр файлов')
        self.showFullScreen()
        self.initLayout()
        self.ioThread = IOThread(lambda signal: self.handleSignal(signal))
        self.ioThread.start()

    def initLayout(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        self.videoWidget = QtMultimediaWidgets.QVideoWidget(self)

        self.mediaPlayer = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        self.mediaPlayer.error.connect(self.handleMediaError)

        logoPath = os.path.join(QtCore.QDir.currentPath(), DATA_DIRNAME, LOGO_FILENAME)
        logoPixmap = QtGui.QPixmap(logoPath)
        self.logoImage = QtWidgets.QLabel()
        self.logoImage.setPixmap(logoPixmap)
        self.errorMessage = QtWidgets.QLabel()
        self.errorMessage.setText('нет доступа')
        self.mainLayout = QtWidgets.QStackedLayout()
        self.mainLayout.addWidget(self.logoImage)    
        self.mainLayout.addWidget(self.errorMessage)  
        self.mainLayout.addWidget(self.videoWidget)  
        self.showLogoLayout()
        centralLayout = QtWidgets.QGridLayout(centralWidget)
        centralLayout.setSpacing(0)
        centralLayout.addLayout(self.mainLayout, 0,0)

    def handleSignal(self, message):
        if message == 1:
            self.useItem(FILENAME, True)
        if message == 2:
            self.useItem(FILENAME1, False)
        if message == 3:
            self.useItem(FILENAME2, True) 
        if message == 4:
            self.useItem(FILENAME3, True)
        if message == 5:
            self.mediaStop()

    def useItem(self,filenameSend,loop):
        self.mediaStop()
        self.loop = loop
        self.sourceFileName = filenameSend
        filename = os.path.join(QtCore.QDir.currentPath(), DATA_DIRNAME, filenameSend)
        self.showVideoLayout()
        self.mediaPlay(filename)

    def showVideoLayout(self):
        self.mediaStop()
        self.mainLayout.setCurrentIndex(2)

    def showLogoLayout(self):
        self.mediaStop()
        self.mainLayout.setCurrentIndex(0)

    def mediaStop(self):
        self.mediaPlayer.stop()

    def handleMediaStatusChanged(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            if self.loop == True:
                filename = os.path.join(QtCore.QDir.currentPath(), DATA_DIRNAME, self.sourceFileName)
                self.showVideoLayout()
                self.mediaPlay(filename)
      
    def mediaPlay(self, filename):
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(filename)))
        self.mediaPlayer.play()

    def handleMediaError(self):
        print('MEDIA ERROR', self.mediaPlayer.errorString())

def runApp():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
    del app

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN_STARTPOZNAVATVIDEO, GPIO.IN)
    GPIO.setup(IN_STARTSOBRANIEVIDEO, GPIO.IN)
    GPIO.setup(IN_ARDSTARTVIDEO, GPIO.IN)
    GPIO.setup(IN_ARDSTOPVIDEO, GPIO.IN)
    GPIO.setup(IN_ARDSTOPVIDEO, GPIO.IN)
    runApp() 
    sys.exit(app.exec_())