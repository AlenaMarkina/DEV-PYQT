"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

+- 1. Возможность перемещения окна по заданным координатам.
- 2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов    +
    * Текущее основное окно    +  # TODO: может экан, а не окно ?
    * Разрешение экрана    +
    * На каком экране окно находится    -
    * Размеры окна  +
    * Минимальные размеры окна  +
    * Текущее положение (координаты) окна   +
    * Координаты центра приложения  -
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
- 3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QScreen

from home_work_2.ui.c_signals_events import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """

        :return:
        """

        self.ui.spinBoxX.setMinimumWidth(50)
        self.ui.spinBoxY.setMinimumWidth(50)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoordsClicked)
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)


    def onPushButtonMoveCoordsClicked(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonMoveCoords

        :return: None
        """

        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()

        self.move(x, y)

    def onPushButtonGetDataClicked(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonGetData

        :return: None
        """

        self.ui.plainTextEdit.appendPlainText(self.screenNumber())
        self.ui.plainTextEdit.appendPlainText(self.currentScreen())
        self.ui.plainTextEdit.appendPlainText(self.screenResolution())
        self.ui.plainTextEdit.appendPlainText(self.windowSize())
        self.ui.plainTextEdit.appendPlainText(self.minWindowSize())
        self.ui.plainTextEdit.appendPlainText(self.currentWindowPos())
        self.ui.plainTextEdit.appendPlainText(self.appCenterPos())
        self.ui.plainTextEdit.appendPlainText(self.windowCurrentState())

    def screenNumber(self):
        """
        Определяет количество экранов

        :return:
        """

        return f'Кол-во экранов: {len(QGuiApplication.screens())}'

    def currentScreen(self):
        """
        Определяет текущее основное окно

        :return:
        """

        #  PySide6.QtGui.QGuiApplication.primaryScreen: PySide6.QtGui.QScreen
        # print(QGuiApplication.screens())  # [<PySide6.QtGui.QScreen(0x1c4d1901b80, name="PL2792Q (1)") at 0x000001C4D20AA5C0>,
        #                                   # <PySide6.QtGui.QScreen(0x1c4d1901ee0, name="PL2792Q (2)") at 0x000001C4D20AA580>]
        # print(QGuiApplication.primaryScreen().name())

        return f'Текущее основное окно: {QGuiApplication.primaryScreen().name()}'

    def screenResolution(self):
        """
        Разрешение экрана в пикселях

        :return:
        """

        width = self.screen().size().width()
        height = self.screen().size().height()

        return f'Разрешение экрана: {width} x {height}'

    def windowSize(self) -> str:
        """
        Определение размеров окна (ширина, высота)

        :return: str
        """

        width = self.size().width()
        height = self.size().height()

        return f'Размеры окна: ширина - {width}, высота - {height}'

    def minWindowSize(self) -> str:
        """
        Определение минимальных размеров окна (ширина, высота)

        :return: str
        """

        min_width = self.minimumSize().width()
        min_height = self.minimumSize().height()

        return f'Минимальные размеры окна: ширина - {min_width}, высота - {min_height}'

    def currentWindowPos(self) -> str:
        """
        Определение текущего положения (координаты) окна (x, y)

        :return: str
        """

        x = self.pos().x()
        y = self.pos().y()

        return f'Текущее положение (координаты) окна: ({x}, {y})'

    def appCenterPos(self) -> str:
        """
        Координаты центра приложения

        :return: str
        """

        return f'Координаты центра приложения: НЕ ДОДЕЛАЛА !!!!!!!!!'

    def windowCurrentState(self):
        """
        Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)

        :return:
        """

        # print(self.windowState().WindowNoState)
        return f'Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено): НЕ ДОДЕЛАЛА !!!!!!!!!'

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
