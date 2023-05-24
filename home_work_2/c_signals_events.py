"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

+ 1. Возможность перемещения окна по заданным координатам.

+ 2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов    +
    * Текущее основное окно    +
    * Разрешение экрана    +
    * На каком экране окно находится    +
    * Размеры окна  +
    * Минимальные размеры окна  +
    * Текущее положение (координаты) окна   +
    * Координаты центра приложения  +
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)  +   Перенесла в 3ий пункт

+ 3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию +
    * При изменении размера окна выводить его новый размер +
"""

from typing import Tuple
from datetime import datetime

from PySide6.QtCore import QEvent
from PySide6 import QtWidgets
from PySide6.QtGui import QGuiApplication, QMoveEvent, QResizeEvent, QHideEvent, QShowEvent

from home_work_2.ui.c_signals_events import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.timestamp = f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}:'

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Доинициализация окна

        :return: None
        """

        self.ui.spinBoxX.setMinimumWidth(50)
        self.ui.spinBoxY.setMinimumWidth(50)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.ui.pushButtonLT.clicked.connect(self.onPushButtonLT)
        self.ui.pushButtonRT.clicked.connect(self.onPushButtonRT)
        self.ui.pushButtonCenter.clicked.connect(self.onPushButtonCenter)
        self.ui.pushButtonLB.clicked.connect(self.onPushButtonLB)
        self.ui.pushButtonRB.clicked.connect(self.onPushButtonRB)

        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoordsClicked)
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)

    # slots --------------------------------------------------------------
    def onPushButtonLT(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonLT

        :return: None
        """
        x, y = 0, 0

        self.move(x, y)

    def onPushButtonRT(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonRT

        :return: None
        """

        screen_width, _ = self.screenResolution()
        window_width, _ = self.windowSize()

        x = screen_width - window_width
        y = 0

        self.move(x, y)

    def onPushButtonCenter(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonCenter

        :return: None
        """

        screen_width, screen_height = self.screenResolution()
        window_width, window_height = self.windowSize()

        x = int(screen_width / 2 - window_width / 2)
        y = int(screen_height / 2 - window_height / 2)

        self.move(x, y)

    def onPushButtonLB(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonLB

        :return: None
        """

        _, screen_height = self.screenResolution()
        _, window_height = self.windowSize()

        x = 0
        y = screen_height - window_height

        self.move(x, y)

    def onPushButtonRB(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonRB

        :return: None
        """

        screen_width, screen_height = self.screenResolution()
        window_width, window_height = self.windowSize()

        x = screen_width - window_width
        y = screen_height - window_height

        self.move(x, y)

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

        log_list = [self.timestamp]

        screen_number = self.screenNumber()
        log_list.append(f'Кол-во экранов:  {screen_number}')

        current_screen = self.currentScreen()
        log_list.append(f'Текущий основной экран:  {current_screen}')

        resolution_width, resolution_height = self.screenResolution()
        log_list.append(f'Разрешение экрана:  {resolution_width} x {resolution_height}')

        log_list.append(f'Окно находится на экране: {self.windowOnWhichScreen()}')

        current_width, currrent_height = self.windowSize()
        log_list.append(f'Размеры окна:  ширина - {current_width}, высота - {currrent_height}')

        min_width, min_height = self.minWindowSize()
        log_list.append(f'Минимальные размеры окна:  ширина - {min_width}, высота - {min_height}')

        current_x, current_y = self.currentWindowPos()
        log_list.append(f'Текущее положение (координаты) окна:  ({current_x}, {current_y})')

        window_center_x, window_center_y = self.appCenterPos()
        log_list.append(f'Координаты центра приложения:  ({window_center_x}, {window_center_x})')

        self.ui.plainTextEdit.appendPlainText('\n       '.join(log_list) + '\n')

    # ---------------------------------------------------------------------
    def screenNumber(self) -> int:
        """
        Определение количества экранов

        :return: int
        """

        return len(QGuiApplication.screens())

    def currentScreen(self) -> str:
        """
        Определение текущего основного экрана

        :return: str
        """

        return QGuiApplication.primaryScreen().name()

    def screenResolution(self) -> Tuple[int, int]:
        """
        Определение разрешения экрана в пикселях

        :return: Tuple[int, int]
        """

        width = self.screen().size().width()
        height = self.screen().size().height()

        return width, height

    def windowOnWhichScreen(self) -> str:
        """
        Определение экрана, на котором находится окно

        :return: str
        """

        return self.screen().name()

    def windowSize(self) -> Tuple[int, int]:
        """
        Определение размеров окна (ширина, высота)

        :return: Tuple[int, int]
        """

        width = self.size().width()
        height = self.size().height()

        return width, height

    def minWindowSize(self) -> Tuple[int, int]:
        """
        Определение минимальных размеров окна (ширина, высота)

        :return: Tuple[int, int]
        """

        min_width = self.minimumSize().width()
        min_height = self.minimumSize().height()

        return min_width, min_height

    def currentWindowPos(self) -> Tuple[int, int]:
        """
        Определение текущего положения (координаты) окна (x, y)

        :return: Tuple[int, int]
        """

        x = self.pos().x()
        y = self.pos().y()

        return x, y

    def appCenterPos(self) -> Tuple[int, int]:
        """
        Определение координат центра приложения

        :return: Tuple[int, int]
        """

        window_cur_x, window_cur_y = self.currentWindowPos()
        window_cur_width, window_cur_height = self.windowSize()

        center_x = int(window_cur_x + window_cur_width / 2)
        center_y = int(window_cur_y + window_cur_height / 2)

        return center_x, center_y

    # events ---------------------------------------------------------------
    # TODO: возможно неверно сделала отслеживание активно/неактивно окно. Не поняла как по-другому сделать.
    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.WindowActivate:
            print(f'{self.timestamp} Окно активно')
        if event.type() == QEvent.Type.WindowDeactivate:
            print(f'{self.timestamp} Окно неактивно')
        return super().event(event)

    def moveEvent(self, event: QMoveEvent) -> None:
        """
        Отслеживание события 'изменения положения окна'

        :param event: QMoveEvent
        :return: None
        """

        old_x, old_y = event.oldPos().x(), event.oldPos().y()
        new_x, new_y = event.pos().x(), event.pos().y()

        print(f'{self.timestamp} Прежние координаты окна {old_x, old_y}, текущие координаты окна {new_x, new_y}')

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Отслеживание события 'изменение размера окна'

        :param event: QResizeEvent
        :return: None
        """

        new_width, new_height = event.size().width(), event.size().height()

        print(f'{self.timestamp} Новый размер окна {new_width, new_height}')

    def hideEvent(self, event: QHideEvent) -> None:
        """
        Отслеживание события 'окно свернуто'

        :param event: QHideEvent
        :return: None
        """

        print(f'{self.timestamp} Окно было свернуто')

    def showEvent(self, event: QShowEvent) -> None:
        """
        Отслеживание события 'окно развернуто'

        :param event: QShowEvent
        :return:None
        """

        print(f'{self.timestamp} Окно было развернуто')


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
