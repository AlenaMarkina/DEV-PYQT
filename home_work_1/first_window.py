from PySide6 import QtWidgets, QtCore

# TODO: add requirements.txt to the repository !!!!!!! pip freeze > requirements.txt
# TODO: посмотерть видео примерно с 24 минуты, там про структуру репозитория
# TODO: directory utils типо для бэкеда например, у нас это папка сервисы или таски и тд


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self) -> None:
        """
        Доинициализация Ui

        :return: None
        """

        self.setWindowTitle('Вход в приложение')
        window_size = QtCore.QSize(500, 200)
        self.setFixedSize(window_size)

        labelLogin = QtWidgets.QLabel()
        labelLogin.setMinimumWidth(50)
        labelLogin.setText('Логин')
        labelPassword = QtWidgets.QLabel()
        labelPassword.setMinimumWidth(50)
        labelPassword.setText('Пароль')

        self.lineEditLogin = QtWidgets.QLineEdit()
        self.lineEditPassword = QtWidgets.QLineEdit()
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.pushButtonRegistration = QtWidgets.QPushButton()
        self.pushButtonRegistration.setText('Регистрация')

        self.pushButtonOk = QtWidgets.QPushButton()
        self.pushButtonOk.setText('OK')

        self.pushButtonCancel = QtWidgets.QPushButton()
        self.pushButtonCancel.setText('Отмена')

        layoutLogin = QtWidgets.QHBoxLayout()
        layoutLogin.addWidget(labelLogin)
        layoutLogin.addWidget(self.lineEditLogin)

        layoutPassword = QtWidgets.QHBoxLayout()
        layoutPassword.addWidget(labelPassword)
        layoutPassword.addWidget(self.lineEditPassword)

        layoutRegistration = QtWidgets.QHBoxLayout()
        layoutRegistration.addSpacerItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Expanding))
        layoutRegistration.addWidget(self.pushButtonRegistration)

        layoutHandle = QtWidgets.QHBoxLayout()
        layoutHandle.addSpacerItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Expanding))
        layoutHandle.addWidget(self.pushButtonOk)
        layoutHandle.addWidget(self.pushButtonCancel)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutLogin)
        layoutMain.addLayout(layoutPassword)
        layoutMain.addLayout(layoutRegistration)
        layoutMain.addLayout(layoutHandle)

        self.setLayout(layoutMain)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = LoginWindow()
    window.show()

    app.exec()
