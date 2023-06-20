from datetime import datetime

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDateTimeEdit, QLabel, QPushButton, QPlainTextEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QColor


class NewNote(QtWidgets.QWidget):
    def __init__(self, thread, parent=None):
        super().__init__(parent)

        self.thread = thread

        self.note_id = 1
        self.notes_dict = {}

        self.initUi()
        self.initSignal()

    def initUi(self):
        self.setMinimumSize(500, 500)

        # plainTextEdit --------------------------------------------------------
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setMaximumSize(400, 500)
        self.plainTextEdit.setPlaceholderText('Введите текст')

        # dateTimeEdit --------------------------------------------------------
        self.labelExpiryDate = QLabel()
        self.labelExpiryDate.setText('Введите дату окончания')

        # dateTimeEdit --------------------------------------------------------
        self.dateTimeEdit = QDateTimeEdit()

        # pushButton -----------------------------------------------------------
        self.pushButtonSaveNote = QPushButton()
        self.pushButtonSaveNote.setText('Сохранить заметку')
        self.pushButtonSaveNote.setMaximumSize(150, 50)

        layoutDate = QHBoxLayout()
        layoutDate.addWidget(self.labelExpiryDate)
        layoutDate.addWidget(self.dateTimeEdit)

        layoutNote = QVBoxLayout()
        layoutNote.addWidget(self.plainTextEdit)
        layoutNote.addLayout(layoutDate)
        layoutNote.addWidget(self.pushButtonSaveNote)

        layoutMain = QHBoxLayout()
        layoutMain.addLayout(layoutNote)

        self.setLayout(layoutMain)

    def initSignal(self):
        self.pushButtonSaveNote.clicked.connect(self.onPushButtonSaveNote)

    def onPushButtonSaveNote(self):
        text = self.plainTextEdit.toPlainText()
        current_date = datetime.now().strftime('%d.%m.%Y %H:%M')  # 18.06.2023 15:53
        expiry_date = self.dateTimeEdit.dateTime().toString('dd.MM.yyyy hh:mm')  # yyyy-MM-dd

        self.notes_dict[f'button_{self.note_id}'] = {'create_note_time': current_date,
                                                     'expiry_date': expiry_date,
                                                     'time_delta': '',
                                                     'note': text}

        self.thread.save_json(self.notes_dict)

        default_time = QDateTimeEdit().dateTime()

        self.dateTimeEdit.setDateTime(default_time)
        self.plainTextEdit.setPlainText('')
        self.note_id += 1
        self.close()


if __name__ == '__main__':
    pass
