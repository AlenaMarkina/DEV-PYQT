"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
+ 1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
   реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit, \
	QHBoxLayout, QVBoxLayout

from a_threads import SystemInfo


class MyWindow(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.initUi()

	def initUi(self):
		self.setMinimumSize(500, 300)

		labelTimeDelay = QLabel()
		labelTimeDelay.setText('Введите время задержки')
		# labelTimeDelay.setFixedSize(188, 30)

		self.lineEditTimeDelay = QLineEdit()
		# self.lineEditTimeDelay.setFixedSize(70, 30)

		self.textEdit = QTextEdit()
		# self.textEdit.setFixedSize(200, 50)

		layoutTimeDelay = QHBoxLayout()
		layoutTimeDelay.addWidget(labelTimeDelay)
		layoutTimeDelay.addWidget(self.lineEditTimeDelay)

		layotTextEdit = QHBoxLayout()
		layotTextEdit.addWidget(self.textEdit)

		layoutMain = QVBoxLayout()
		layoutMain.addLayout(layoutTimeDelay)
		layoutMain.addLayout(layotTextEdit)

		self.setLayout(layoutMain)



	def initThread(self):
		pass

	def initSignals(self):
		pass


if __name__ == '__main__':
	app = QApplication()

	window = MyWindow()
	window.show()

	app.exec()
