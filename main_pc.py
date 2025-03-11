import os
import sys
from time import sleep

from PyQt6 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets


# Определение клавиш клавиатуры
KEY_STARTPOZNAVATVIDEO = QtCore.Qt.Key.Key_1
KEY_STARTSOBRANIEVIDEO = QtCore.Qt.Key.Key_2
KEY_ARDLOGOVIDEO = QtCore.Qt.Key.Key_3
KEY_ARDSTARTVIDEO = QtCore.Qt.Key.Key_4
KEY_ARDSTOPVIDEO = QtCore.Qt.Key.Key_5
trig = True
DATA_DIRNAME = 'media'
LOGO_FILENAME = 'logo.jpg'
FILENAME = '0001_fixed.mp4'
FILENAME2 = '4_fixed.mp4'
FILENAME1 = 'Совет.mp4'
FILENAME3 = '3333.mp4'


import os
import sys
from PyQt6 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.loop = False
        self.sourceFileName = ''
        self.setMinimumSize(QtCore.QSize(800, 640))
        self.setWindowTitle('Просмотр файлов')
        self.showFullScreen()
        self.initLayout()

    def initLayout(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainLayout = QtWidgets.QStackedLayout()  # Создаём layout только один раз

        # Устанавливаем ЧЕРНЫЙ фон для всего окна
        self.setStyleSheet("background-color: black;")

        # Загрузка GIF-анимации
        self.logoAnimation = QtWidgets.QLabel(self)
        self.logoMovie = QtGui.QMovie(os.path.join(DATA_DIRNAME, "logo_animation.gif"))  # Загружаем GIF
        self.logoAnimation.setMovie(self.logoMovie)
        self.logoAnimation.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Центрируем анимацию
        self.logoAnimation.setStyleSheet("background-color: black;")  # ЧЕРНЫЙ фон
        self.mainLayout.addWidget(self.logoAnimation)  # Добавляем в layout

        # Настройка видеоплеера
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        self.videoWidget = QtMultimediaWidgets.QVideoWidget(self)
        self.videoWidget.setStyleSheet("background-color: black;")  # ЧЕРНЫЙ фон для видео
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mainLayout.addWidget(self.videoWidget)  # Добавляем в layout

        # Подключаем сигнал
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        print("Сигнал mediaStatusChanged подключён!")  # Логирование подключения


        # Логотип компании
        logoPath = os.path.join(QtCore.QDir.currentPath(), DATA_DIRNAME, LOGO_FILENAME)
        logoPixmap = QtGui.QPixmap(logoPath)
        self.logoImage = QtWidgets.QLabel()
        self.logoImage.setPixmap(logoPixmap)
        self.logoImage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Центрируем логотип
        self.logoImage.setStyleSheet("background-color: black;")  # ЧЕРНЫЙ фон
        self.mainLayout.addWidget(self.logoImage)  # Добавляем логотип

        # Сообщение об ошибке
        self.errorMessage = QtWidgets.QLabel()
        self.errorMessage.setText('Нет доступа')
        self.errorMessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Центрируем текст
        self.errorMessage.setStyleSheet(
            "background-color: black; color: red; font-size: 20px;")  # ЧЕРНЫЙ фон + красный текст
        self.mainLayout.addWidget(self.errorMessage)

        # Устанавливаем центральный layout
        centralLayout = QtWidgets.QGridLayout(centralWidget)
        centralLayout.setSpacing(0)
        centralLayout.addLayout(self.mainLayout, 0, 0)

        self.showLogoLayout()  # Показываем логотип при запуске

    def keyPressEvent(self, event):
        global trig
        key = event.key()
        print(f"Нажата клавиша: {key}")  # Логирование клавиши
        if key == KEY_STARTPOZNAVATVIDEO:
            self.useItem(FILENAME, True)
        elif key == KEY_STARTSOBRANIEVIDEO and trig:
            trig=False
            self.useItem(FILENAME1, True)
        elif key == KEY_ARDLOGOVIDEO:
            self.showAnimation()  # Показываем анимацию
        elif key == KEY_ARDSTARTVIDEO:
            self.useItem(FILENAME3, True)
        elif key == KEY_ARDSTOPVIDEO:
            trig = True
            self.mediaStop()  # Останавливаем видео
            self.logoMovie.stop()  # Останавливаем анимацию

    def showAnimation(self):
        self.mediaStop()
        self.mainLayout.setCurrentWidget(self.logoAnimation)  # Переключаемся на анимацию
        self.logoMovie.start()  # Запускаем анимацию


    def useItem(self, filenameSend, loop):
        self.loop = loop
        self.sourceFileName = filenameSend
        filename = os.path.abspath(os.path.join(DATA_DIRNAME, filenameSend))

        if not os.path.exists(filename):
            print(f"Ошибка: Файл {filename} не найден!")
            return

        print(f"Запуск видео: {filename}")
        self.showVideoLayout()
        self.mediaPlay(filename)

    def showVideoLayout(self):
        print("Переключение на видео")
        self.mainLayout.setCurrentWidget(self.videoWidget)  # Переключаемся на видео

    def showLogoLayout(self):
        print("Переключение на логотип")
        if self.mediaPlayer.mediaStatus() != QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaStop()
        self.mainLayout.setCurrentWidget(self.logoImage)

    def mediaStop(self):
        print("Остановка видео")
        self.mediaPlayer.stop()

    def handleMediaStatusChanged(self, status):
        print(f"Статус видео изменился: {status}")

        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            print("Видео завершено.")
            if self.sourceFileName == FILENAME:
                print("Повторное воспроизведение видео")
                self.useItem(self.sourceFileName, True)  # Повторное воспроизведение бесконечно
            else:
                print("Переключаемся на логотип через 2 сек.")
                QtCore.QTimer.singleShot(2000, self.showLogoLayout)

    def mediaPlay(self, filename):
        if not os.path.exists(filename):
            print(f"Ошибка: Файл {filename} не найден!")
            return
        print(f"Запуск видео: {filename}")
        self.mediaPlayer.setSource(QtCore.QUrl.fromLocalFile(filename))
        self.mediaPlayer.play()

    def handleMediaError(self):
        print(f'MEDIA ERROR: {self.mediaPlayer.errorString()}')


def runApp():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    runApp()
