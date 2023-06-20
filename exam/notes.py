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
from typing import Tuple
import os
from json_thread import JsonThread
from new_note import NewNote
from functools import partial
import json
import pprint


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.push_button_list = []
        self.which_button_pressed = None
        self.thread = None

        self.initUi()
        self.initThread()
        self.new_note_window = NewNote(self.thread)
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация окна

        :return: None
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
        self.pushButtonCreateNewNote = QPushButton()
        self.pushButtonCreateNewNote.setText('Добавить заметку')
        self.pushButtonCreateNewNote.setMaximumSize(150, 50)

        self.pushButtonSaveChanges = QPushButton()
        self.pushButtonSaveChanges.setText('Сохранить изменения')
        self.pushButtonSaveChanges.setMaximumSize(150, 50)

        # plainTextEdit --------------------------------------------------------
        self.plainTextEdit = QPlainTextEdit()
        # self.plainTextEdit.setMaximumSize(400, 500)
        self.plainTextEdit.setPlaceholderText('Предварительный просмотр')

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.addWidget(self.pushButtonCreateNewNote, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.layoutFrame.addWidget(self.pushButtonSaveChanges, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        self.frameNewNote.setLayout(self.layoutFrame)

        layoutFrame1 = QHBoxLayout()
        layoutFrame1.addWidget(self.frameNewNote)
        layoutFrame1.addWidget(self.plainTextEdit)

        layoutMain = QHBoxLayout()
        layoutMain.addLayout(layoutFrame1)

        self.setLayout(layoutMain)

    def initThread(self) -> None:
        """
        Инициализация потока

        :return: None
        """
        self.thread = JsonThread()
        self.thread.start()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.pushButtonCreateNewNote.clicked.connect(self.onPushButtonCreateNewNote)
        self.pushButtonSaveChanges.clicked.connect(self.onPushButtonSaveChanges)
        self.new_note_window.new_note_signal.connect(self.newNoteSignalHandle)
        self.thread.data.connect(lambda x: print(x))  # {'button_1': [-8572, 8, 36], 'button_2': [-8572, 8, 36], 'button_3': [-8572, 8, 36]}

    # slots --------------------------------------------------------------
    def onPushButtonCreateNewNote(self) -> None:
        """
        Создание и размещение новой кнопки на панели и подключение к ней сигнала 'clicked'

        :return: None
        """
        self.new_note_window.show()

    def newNoteSignalHandle(self, data: Tuple[str, str]) -> None:
        """
        Обработка сигнала из дочернего окна 'new_note_window':

        - создание и размещение новой кнопки на панели;
        - подключение к кнопке сигнала 'clicked';
        - подключение к кнопке фильтра событий 'installEventFilter'

        :param data: Кортеж из заголовка заметки и названия кнопки, которая ассоциируется с этой заметкой
        :return: None
        """
        note_title, button_name = data  # 'harry', 'note_1'

        pushButton = QPushButton()
        pushButton.setMaximumSize(120, 50)
        pushButton.setAccessibleName(button_name)
        pushButton.setText(note_title)

        pushButton.clicked.connect(partial(self.onPushButton, pushButton))
        pushButton.installEventFilter(self)

        self.push_button_list.append(pushButton)
        self.layoutFrame.addWidget(pushButton, )

    def onPushButton(self, button: QPushButton) -> None:
        """
        Обработка сигнала 'clicked' для кнопки, которая ассоциируется с заметкой

        :param button: QPushButton
        :return: None
        """
        print()
        text = self.thread.load_json()

        self.plainTextEdit.setPlainText(text[f'{button.accessibleName()}']['note'])
        self.which_button_pressed = button

        pprint.pprint(self.new_note_window.notes_dict)
        print()

    def onPushButtonSaveChanges(self) -> None:
        """
        Обработка сигнала 'clicked' для кнопки pushButtonSaveChanges

        :return: None
        """
        text = self.plainTextEdit.toPlainText()
        self.new_note_window.notes_dict[f'{self.which_button_pressed.accessibleName()}']['note'] = text
        self.thread.save_json(self.new_note_window.notes_dict)

    def show_message_question(self, watched) -> None:
        """
        Работа с окном QtWidgets.QMessageBox.question

        :return: None
        """
        answer = QtWidgets.QMessageBox.question(self, "Удаление заметки", "Удалить заметку ?")

        if answer == QtWidgets.QMessageBox.Yes:
            # Remove note from note_dict.
            button_name = watched.accessibleName()
            self.new_note_window.notes_dict.pop(button_name)
            self.thread.save_json(self.new_note_window.notes_dict)

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
