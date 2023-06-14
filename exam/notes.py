from PySide6 import QtWidgets


class MyWindow(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.initUi()

	def initUi(self) -> None:
		"""

		:return:
		"""
		self.setWindowTitle('Заметки')
		self.mdiAria = QtWidgets.QMdiArea()

		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(self.mdiAria)

		layoutMain = QtWidgets.QHBoxLayout()
		layoutMain.addLayout(layout)

		self.setLayout(layoutMain)

	def initSignals(self) -> None:
		"""

		:return:
		"""
		pass


if __name__ == '__main__':
	app = QtWidgets.QApplication()

	window = MyWindow()
	window.show()

	app.exec()
