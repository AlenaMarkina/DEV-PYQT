"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QObject

from home_work_2.ui.d_eventfilter_settings import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.initSignal()

    def initUi(self):
        """

        :return:
        """

        self.setMinimumSize(600, 600)
        self.ui.comboBox.addItems(['oct', 'hex', 'bin', 'dec'])

    def initSignal(self):
        """

        :return:
        """

        # self.ui.dial.valueChanged

        self.ui.comboBox.textActivated.connect(self.onComboBoxTextActivated)

        # self.ui.dial.installEventFilter(self)

    def onComboBoxTextActivated(self):
        number_system = self.ui.comboBox.currentText()
        if number_system == 'hex':
            pass
            # TODO set the hex mode to lcdNumber
            # self.ui.lcdNumber.display()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """

        :param watched:
        :param event:
        :return:
        """

        if watched == self.ui.dial and event.type() == QEvent.Type.KeyPress:
            print(event.key())
            print(event.type().value())

        return super(Window, self).eventFilter(watched, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
