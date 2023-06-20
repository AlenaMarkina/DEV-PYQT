"""
Реализовать приложение для работы с заметками

Обязательные функции в приложении:
+- * Добавление, изменение, удаление заметок
+- * Сохранение времени добавления заметки и отслеживание времени до дэдлайна.
+ * Реализация хранения заметок остаётся на ваш выбор (БД, json и т.д.).
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFrame, QPushButton, QPlainTextEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QColor
import PySide6
import time
import os
from json_thread import JsonThread
from new_note import NewNote
from functools import partial
import json
import pprint


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.button_counter: int = 0
        self.push_button_list = []
        self.which_button_pressed = None
        self.pushButton = None
        self.thread = None

        self.initUi()
        self.initThread()
        self.initSignals()

        self.note_window = NewNote(self.thread)

    def initUi(self) -> None:
        """

        :return:
        """
        self.setWindowTitle('Заметки')
        self.setMinimumSize(400, 400)

        # frame ---------------------------------------------------------------
        self.frameNewNote = QFrame()
        # self.frameNewNote.setMaximumSize(200, 500)
        self.frameNewNote.setMinimumWidth(200)
        self.frameNewNote.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        # self.frameNewNote.setContentsMargins(1, 5, 0, 5)

        # pushButton -----------------------------------------------------------
        self.pushButtonSaveChanges = QPushButton()
        self.pushButtonSaveChanges.setText('Сохранить изменения')
        self.pushButtonSaveChanges.setMaximumSize(150, 50)

        self.pushButtonNewNote = QPushButton()
        self.pushButtonNewNote.setText('Добавить заметку')
        self.pushButtonNewNote.setMaximumSize(150, 50)

        # plainTextEdit --------------------------------------------------------
        self.plainTextEdit = QPlainTextEdit()
        # self.plainTextEdit.setMaximumSize(400, 500)
        self.plainTextEdit.setPlaceholderText('Предварительный просмотр')

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.addWidget(self.pushButtonNewNote, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.layoutFrame.addWidget(self.pushButtonSaveChanges, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        self.frameNewNote.setLayout(self.layoutFrame)

        layoutFrame1 = QHBoxLayout()
        layoutFrame1.addWidget(self.frameNewNote)
        layoutFrame1.addWidget(self.plainTextEdit)

        layoutMain = QHBoxLayout()
        layoutMain.addLayout(layoutFrame1)

        self.setLayout(layoutMain)

    def initThread(self):
        self.thread = JsonThread()
        self.thread.start()

    def initSignals(self) -> None:
        """
        :return:
        """
        self.pushButtonNewNote.clicked.connect(self.onPushButtonCreateNote)
        self.pushButtonSaveChanges.clicked.connect(self.plainTextEditChanged)
        self.thread.data.connect(
            lambda x: print(x))  # {'button_1': [-8572, 8, 36], 'button_2': [-8572, 8, 36], 'button_3': [-8572, 8, 36]}

    # self.plainTextEdit.textChanged.connect(self.onPushButtonNewNote)

    # slots --------------------------------------------------------------
    def onPushButtonCreateNote(self):
        """
        Создание и размещение новой кнопки на панели и подключение к ней сигнала 'clicked'

        :return: None
        """
        self.note_window.show()
        self.button_counter += 1

        pushButton = QPushButton()
        pushButton.setMaximumSize(120, 50)
        pushButton.setAccessibleName(f'button_{self.button_counter}')
        pushButton.setText(f'button_{self.button_counter}')
        pushButton.clicked.connect(partial(self.onPushButtonNote, pushButton))
        pushButton.installEventFilter(self)

        # pushButton.mouseDoubleClickEvent(PySide6.QtGui.QMouseEvent(type=QtCore.QEvent.Type.MouseButtonDblClick))
        self.push_button_list.append(pushButton)

        self.layoutFrame.addWidget(pushButton, )

    def onPushButtonNote(self, button):
        # {'button_1': {'create_note_time': '19.06.2023 11:48',
        #               'expiry_date': '19.06.2023 15:00',
        #               'note': 'Harry Potter'},
        #  'button_2': {'create_note_time': '19.06.2023 11:49',
        #               'expiry_date': '19.06.2023 16:00',
        #               'note': 'Ron and Hermiona'}}
        print('\nin onPushButtonNote()')
        print(f'    {button.accessibleName()}')

        # отобразили предыдущую запись
        text = self.thread.load_json()
        self.plainTextEdit.setPlainText(text[f'{button.accessibleName()}']['note'])

        self.which_button_pressed = button
        print(self.which_button_pressed)

        pprint.pprint(self.note_window.notes_dict)
        print()

    def plainTextEditChanged(self):
        print('\nin plainTextEditChanged()')
        print(f'    {self.plainTextEdit.toPlainText()}')
        current_text = self.plainTextEdit.toPlainText()
        self.note_window.notes_dict[f'{self.which_button_pressed.accessibleName()}']['note'] = current_text
        self.thread.save_json(self.note_window.notes_dict)

        print()

    def show_message_question(self, watched) -> None:
        """
        Работа с окном QtWidgets.QMessageBox.question

        :return: None
        """
        answer = QtWidgets.QMessageBox.question(self, "Удаление заметки", "Удалить заметку ?")

        if answer == QtWidgets.QMessageBox.Yes:
            # Remove note from note_dict.
            button_name = watched.accessibleName()
            self.note_window.notes_dict.pop(button_name)
            self.thread.save_json(self.note_window.notes_dict)

            # Remove note from the button_list and the app.
            note_idx = self.push_button_list.index(watched)
            self.push_button_list.pop(note_idx)
            self.layoutFrame.removeWidget(watched)

        elif answer == QtWidgets.QMessageBox.No:
            pass

    # events --------------------------------------------------------------
    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        if watched in self.push_button_list and event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                # self.show_message_question(watched)
                print(event.button())
        return super(MyWindow, self).eventFilter(watched, event)

    # TODO: как корректно закрыть поток ?
    # 		у меня в потоке есть delay и поэтому поток не реагирует, если я меняю status на False
    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        path_ = ''.join([os.path.abspath(os.getcwd()), '/my_notes'])
        print(path_)
        os.remove(path_)
        self.thread.status = False
        self.thread.quit()

        print('close event')


# {'button_1': {'create_note_time': '19.06.2023 21:16',
#               'expiry_date': '01.01.2000 00:00',
#               'note': 'f'},
#  'button_2': {'create_note_time': '19.06.2023 21:16',
#               'expiry_date': '01.01.2000 00:00',
#               'note': 'y'}}

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = MyWindow()
    window.show()

    app.exec()
