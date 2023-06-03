"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

+ 1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

+ 2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

+ 3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

+ 4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QEvent, QObject
from PySide6.QtGui import QCloseEvent

from home_work_2.ui.d_eventfilter_settings import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings("HomeWork2")

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.loadData()
        self.initSignal()

    def initUi(self) -> None:
        """
        Доинициализация окна

        :return: None
        """
        self.setMinimumSize(600, 600)
        self.ui.comboBox.addItems(['oct', 'hex', 'bin', 'dec'])
        self.ui.dial.installEventFilter(self)

    def initSignal(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.ui.dial.valueChanged.connect(self.onDialValueChanged)
        self.ui.horizontalSlider.valueChanged.connect(self.onSliderValueChanged)
        self.ui.comboBox.textActivated.connect(self.onComboBoxTextActivated)

    # slots --------------------------------------------------------------
    def onComboBoxTextActivated(self) -> None:
        """
        Обработка сигнала 'textActivated' для виджета comboBox
        :return: None
        """
        mode = self.ui.comboBox.currentText()

        if mode == 'bin':
            self.ui.lcdNumber.setBinMode()
        elif mode == 'hex':
            self.ui.lcdNumber.setHexMode()
        elif mode == 'oct':
            self.ui.lcdNumber.setOctMode()
        elif mode == 'dec':
            self.ui.lcdNumber.setDecMode()

    def onSliderValueChanged(self) -> None:
        """
        Обработка сигнала 'valueChanged' для виджета horizontalSlider
        :return: None
        """
        num = self.ui.horizontalSlider.value()

        self.ui.lcdNumber.display(num)
        self.ui.dial.setSliderPosition(num)

    def onDialValueChanged(self) -> None:
        """
        Обработка сигнала 'valueChanged' для виджета dial
        :return: None
        """
        num = self.ui.dial.value()

        self.ui.lcdNumber.display(num)
        self.ui.horizontalSlider.setSliderPosition(num)

    # events ---------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Событие закрытия окна

        :param event: QCloseEvent
        :return: None
        """
        self.settings.setValue("combox_mode", self.ui.comboBox.currentText())
        self.settings.setValue("lcdNumber_value", self.ui.lcdNumber.intValue())

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
        Обработка событий нажатия кнопок клавиатуры (+ и -) для виджета dial

        :param watched: QObject
        :param event: QEvent
        :return: bool
        """
        # TODO: почему-то для self.ui.dial данное событие срабатывает для всех виджетов,
        #       хотя должно только для self.ui.dial ..
        if watched == self.ui.dial and event.type() == QEvent.Type.KeyPress:
            current_step = watched.value()

            if event.key() == QtCore.Qt.Key.Key_Minus:
                current_step -= watched.singleStep()
                watched.setSliderPosition(current_step)

            if event.key() == QtCore.Qt.Key.Key_Plus:
                current_step += watched.singleStep()
                watched.setSliderPosition(current_step)

        return super(Window, self).eventFilter(watched, event)

    # ---------------------------------------------------------------------
    def loadData(self) -> None:
        """
        Загрузка данных при открытии приложения

        :return: None
        """
        self.ui.lcdNumber.display(self.settings.value('lcdNumber_value', ''))
        self.ui.comboBox.setCurrentText(self.settings.value('combox_mode', ''))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
