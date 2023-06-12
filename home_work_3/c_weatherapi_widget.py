"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
+ 1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
+ 2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
+ 3. поле для вывода информации о погоде в указанных координатах
+ 4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets
from a_threads import WeatherHandler


class WeatherApiWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread = None

        self.initUi()
        self.initThread()
        self.initSignals()

    def initUi(self) -> None:
        """
         Доинициализация окна

        :return: None
        """
        self.setMinimumSize(350, 300)

        labelLatitude = QtWidgets.QLabel()
        labelLatitude.setText('Введите широту')
        labelLongitude = QtWidgets.QLabel()
        labelLongitude.setText('Введите долготу')
        labelTimeDelay = QtWidgets.QLabel()
        labelTimeDelay.setText('Введите время задержки')

        self.lineEditLatitude = QtWidgets.QLineEdit()
        self.lineEditLongitude = QtWidgets.QLineEdit()

        self.spinBoxTimeDelay = QtWidgets.QSpinBox()
        self.spinBoxTimeDelay.setMinimum(1)

        self.plainTextWeather = QtWidgets.QPlainTextEdit()
        self.plainTextWeather.setReadOnly(True)
        self.plainTextWeather.setPlaceholderText('Информация о погоде')

        self.pushButtonStart = QtWidgets.QPushButton()
        self.pushButtonStart.setText('Запустить поток')
        self.pushButtonStop = QtWidgets.QPushButton()
        self.pushButtonStop.setText('Остановить поток')

        layoutGrid = QtWidgets.QGridLayout()
        layoutGrid.addWidget(labelLatitude, 0, 0)
        layoutGrid.addWidget(self.lineEditLatitude, 0, 1)
        layoutGrid.addWidget(labelLongitude, 1, 0)
        layoutGrid.addWidget(self.lineEditLongitude, 1, 1)
        layoutGrid.addWidget(labelTimeDelay, 2, 0)
        layoutGrid.addWidget(self.spinBoxTimeDelay, 2, 1)
        layoutGrid.addWidget(self.plainTextWeather, 3, 0, 1, 2)
        layoutGrid.addWidget(self.pushButtonStart, 4, 0)
        layoutGrid.addWidget(self.pushButtonStop, 4, 1)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutGrid)

        self.setLayout(layoutMain)

    def initThread(self) -> None:
        """
        Инициализация потока

        :return: None
        """
        self.thread = WeatherHandler()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.pushButtonStart.clicked.connect(self.onPushButtonStart)
        self.pushButtonStop.clicked.connect(self.onPushButtonStop)
        self.thread.response.connect(self.updateWeather)

    def onPushButtonStart(self) -> None:
        """
         Обработка сигнала 'clicked' для кнопки pushButtonStart

        :return: None
        """
        self.thread.start()
        print('Поток запущен.')

        try:
            self.thread.latitude = float(self.lineEditLatitude.text())
            self.thread.longitude = float(self.lineEditLongitude.text())
        except ValueError as error:
            print(f'latitude or longitude error: {error}')

        self.thread.delay = self.spinBoxTimeDelay.value()
        self.thread.api_url = (self.thread.latitude, self.thread.longitude)

        self.lineEditLatitude.setReadOnly(True)
        self.lineEditLongitude.setReadOnly(True)
        self.spinBoxTimeDelay.setReadOnly(True)

    def onPushButtonStop(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonStop

        :return: None
        """
        self.thread.status = False

        print('Поток остановлен.')

        self.lineEditLatitude.setReadOnly(False)
        self.lineEditLongitude.setReadOnly(False)
        self.spinBoxTimeDelay.setReadOnly(False)

    def updateWeather(self, data: dict) -> None:
        """
        Обработка данных о погоде из потока

        :param data: Словарь с данными о погоде
        :return: None
        """
        weather = f'Температура {data["current_weather"]["temperature"]} °C, ' \
                  f'скорость ветра {data["current_weather"]["windspeed"]} м/с'

        self.plainTextWeather.appendPlainText(weather)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = WeatherApiWindow()
    window.show()

    app.exec()
