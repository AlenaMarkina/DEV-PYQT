"""
Реализовать приложение для работы с заметками

Обязательные функции в приложении:
+- * Добавление, изменение, удаление заметок
+ * Сохранение времени добавления заметки и отслеживание времени до дэдлайна.
+ * Реализация хранения заметок остаётся на ваш выбор (БД, json и т.д.).
"""

import os
from typing import Tuple
from functools import partial

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QFrame, QPushButton, QPlainTextEdit, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QCloseEvent

from new_note import NewNote
from json_thread import JsonThread


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread = None
        self.which_button_pressed = None
        self.push_button_dict = {}  # {QPushButton: {'label': QLabel, 'layout': QHBoxLayout}}

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
        self.setMinimumSize(800, 500)

        # frame ---------------------------------------------------------------
        self.frameNewNote = QFrame()
        # self.frameNewNote.setMaximumSize(200, 500)
        self.frameNewNote.setMinimumWidth(300)
        self.frameNewNote.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

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
        self.thread.signal.connect(self.threadSignalHandle)

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
        note_title, button_name = data

        label = QLabel()
        label.setText('')

        pushButton = QPushButton()
        pushButton.setMaximumSize(120, 50)
        pushButton.setAccessibleName(button_name)
        pushButton.setText(note_title)

        pushButton.clicked.connect(partial(self.onPushButton, pushButton))
        pushButton.installEventFilter(self)

        # self.push_button_dict[pushButton] = label  # {QPushButton: QLabel}  was

        layout = QHBoxLayout()
        layout.addWidget(pushButton)
        layout.addWidget(label)

        self.push_button_dict[pushButton] = {'label': label, 'layout': layout}  # {QPushButton: {'label': QLabel, 'layout': QHBoxLayout}}
        self.layoutFrame.addLayout(layout)

    def threadSignalHandle(self, data) -> None:
        """
        Обработка сигнала из потока

        :param data:
        :return: None
        """
        # 20.06.2023 21:20
        button_name, days, hours, minutes = data
        is_deadline = list(filter(lambda x: x < 0, [days, hours, minutes]))

        # {QPushButton: {'label': QLabel, 'layout': QHBoxLayout}}
        try:
            label = next((dict_['label'] for btn, dict_ in self.push_button_dict.items() if btn.accessibleName() == button_name))
            if is_deadline:
                label.setText(f'срок выполнения истек!')
            else:
                label.setText(f'дэдлайн через:\n{days} дн. {hours} ч. {minutes} мин')
        except StopIteration as err:
            pass

    def onPushButton(self, button: QPushButton) -> None:
        """
        Обработка сигнала 'clicked' для кнопки, которая ассоциируется с заметкой

        :param button: QPushButton
        :return: None
        """
        text = self.thread.load_json()

        self.plainTextEdit.setPlainText(text[f'{button.accessibleName()}']['note'])
        self.which_button_pressed = button

        import pprint
        print()
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
        self.thread.status = False
        answer = QtWidgets.QMessageBox.question(self, "Удаление заметки", "Удалить заметку ?")

        if answer == QtWidgets.QMessageBox.Yes:

            # Remove note from notes_dict.
            button_name = watched.accessibleName()
            self.new_note_window.notes_dict.pop(button_name)
            self.thread.save_json(self.new_note_window.notes_dict)

            # Remove note from the button_dict.
            # self.push_button_dict.pop(watched)

            # Remove note from the app.
            # self.layoutFrame.removeWidget(watched)  # watched = {QPushButton: {'label': QLabel, 'layout': QHBoxLayout}}
            self.layoutFrame.adoptLayout(self.push_button_dict[watched]['layout'])

        elif answer == QtWidgets.QMessageBox.No:
            pass

    # events --------------------------------------------------------------
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
        Обработка события нажатия правой кнопки мыши для кнопок, которые ассоциируются с заметками

        :param watched: QObject
        :param event: QEvent
        :return: bool
        """
        if watched in self.push_button_dict and event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.show_message_question(watched)
        return super(MyWindow, self).eventFilter(watched, event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Обработка события закрытия приложения

        :param event: QCloseEvent
        :return: None
        """
        path_ = ''.join([os.path.abspath(os.getcwd()), '/my_notes'])
        os.remove(path_)
        self.thread.terminate()


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = MyWindow()
    window.show()

    app.exec()
