from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFrame, QPushButton, QPlainTextEdit, QHBoxLayout
from PySide6.QtGui import QColor
import PySide6


class MyWindow(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.initUi()
		self.initSignals()

	def initUi(self) -> None:
		"""

		:return:
		"""
		self.setWindowTitle('Заметки')
		self.setMinimumSize(850, 550)

		# frame ---------------------------------------------------------------
		self.frameNewNote = QFrame()
		# self.frameNewNote.setMaximumSize(200, 500)
		self.frameNewNote.setMinimumWidth(200)
		self.frameNewNote.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
		# self.frameNewNote.setContentsMargins(1, 5, 0, 5)

		# pushButton -----------------------------------------------------------
		self.pushButtonNewNote = QPushButton()
		self.pushButtonNewNote.setText('Новая заметка')
		self.pushButtonNewNote.setMaximumSize(120, 50)

		# plainTextEdit --------------------------------------------------------
		self.plainTextEdit = QPlainTextEdit()
		# self.plainTextEdit.setMaximumSize(400, 500)
		self.plainTextEdit.setPlaceholderText('Предварительный просмотр')

		layoutPushButton = QHBoxLayout()
		layoutPushButton.addWidget(self.pushButtonNewNote, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

		self.frameNewNote.setLayout(layoutPushButton)

		layoutFrame1 = QHBoxLayout()
		layoutFrame1.addWidget(self.frameNewNote)
		layoutFrame1.addWidget(self.plainTextEdit)

		layoutMain = QHBoxLayout()
		layoutMain.addLayout(layoutFrame1)

		self.setLayout(layoutMain)

	def initSignals(self) -> None:
		"""

		:return:
		"""
		self.pushButtonNewNote.clicked.connect(lambda: self.plainTextEdit.appendPlainText('Harry'))

	# slots --------------------------------------------------------------
	def onPushButtonNewNote(self):
		pass

	# ---------------------------------------------------------------------
	def create_new_button(self):
		self.pushBotton = QPushButton()
		self.pushBotton.set

if __name__ == '__main__':
	app = QtWidgets.QApplication()

	window = MyWindow()
	window.show()

	app.exec()
