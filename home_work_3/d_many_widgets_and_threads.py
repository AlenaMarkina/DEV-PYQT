"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from PySide6 import QtWidgets

from b_systeminfo_widget import SystemInfoWindow
from c_weatherapi_widget import WeatherApiWindow


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.system_info = SystemInfoWindow(parent=self)
        self.weather_api = WeatherApiWindow(parent=self)

        self.initUi()

    def initUi(self):
        layoutGrid = QtWidgets.QGridLayout()
        layoutGrid.addWidget(self.system_info, 0, 0)
        layoutGrid.addWidget(self.weather_api, 0, 1)

        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutGrid)

        self.setLayout(layoutMain)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = MainWindow()
    window.show()

    app.exec()

