from PySide6 import QtWidgets


class MyWindow(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

	def initUi(self) -> None:
		"""

		:return:
		"""
		pass

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