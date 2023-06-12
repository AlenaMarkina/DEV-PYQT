"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
+ 1. поле для ввода времени задержки
+ 2. поле для вывода информации о загрузке CPU
+ 3. поле для вывода информации о загрузке RAM
+ 4. поток необходимо запускать сразу при старте приложения
+ 5. установку времени задержки сделать "горячей", т.е. поток должен сразу
   реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QLabel, QSpinBox, QPlainTextEdit, QVBoxLayout
from PySide6.QtGui import QCloseEvent

from a_threads import SystemInfo


class MyWindow(QtWidgets.QWidget):
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
		self.setMinimumSize(500, 300)

		labelTimeDelay = QLabel()
		labelTimeDelay.setText('Введите время задержки')

		labelCPU = QLabel()
		labelCPU.setText('Загрузка CPU')

		labelRAM = QLabel()
		labelRAM.setText('Загрузка RAM')

		self.spinBox = QSpinBox()
		self.spinBox.setMinimum(1)

		self.textEditCPU = QPlainTextEdit()
		self.textEditCPU.setReadOnly(True)
		self.textEditRAM = QPlainTextEdit()
		self.textEditRAM.setReadOnly(True)

		layoutGrid = QtWidgets.QGridLayout()
		layoutGrid.addWidget(labelTimeDelay, 0, 0)
		layoutGrid.addWidget(self.spinBox, 0, 1)
		layoutGrid.addWidget(labelCPU, 1, 0)
		layoutGrid.addWidget(labelRAM, 1, 1)
		layoutGrid.addWidget(self.textEditCPU, 2, 0)
		layoutGrid.addWidget(self.textEditRAM, 2, 1)

		layoutMain = QVBoxLayout()
		layoutMain.addLayout(layoutGrid)

		self.setLayout(layoutMain)

	def initThread(self) -> None:
		"""
		Инициализация потока

		:return: None
		"""
		self.thread = SystemInfo()
		self.thread.start()

		print('Поток запущен.')

	def initSignals(self) -> None:
		"""
		Инициализация сигналов

		:return: None
		"""
		self.spinBox.textChanged.connect(self.onSpinBoxChanged)
		self.thread.systemInfoReceived.connect(self.threadHandler)

	def threadHandler(self, list_of_data: list) -> None:
		"""
		Обработка данных из потока

		:param list_of_data: Список данных о загрузке CPU и RAM
		:return: None
		"""
		cpu_value, ram_value = list_of_data

		self.textEditCPU.appendPlainText(f'{cpu_value} %')
		self.textEditRAM.appendPlainText(f'{ram_value} %')

	def onSpinBoxChanged(self) -> None:
		"""
		Обработка сигнала 'textChanged' для виджета spinBox

		:return: None
		"""
		delay_number = self.spinBox.value()
		self.thread.delay = delay_number

	def closeEvent(self, event: QCloseEvent) -> None:
		"""
		Обработка события закрытия окна

		:param event: QCloseEvent
		:return: None
		"""
		self.thread.terminate()
		print('Поток закрыт.')


if __name__ == '__main__':
	app = QApplication()

	window = MyWindow()
	window.show()

	app.exec()
