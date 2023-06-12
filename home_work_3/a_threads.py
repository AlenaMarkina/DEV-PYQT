"""
Модуль в котором содержаться потоки Qt
"""

import time
from typing import Optional

import psutil
import requests
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # TODO Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # TODO создайте атрибут класса self.delay = None, для управлением задержкой получения данных

    def run(self) -> None:  # TODO переопределить метод run
        if self.delay is None:  # TODO Если задержка не передана в поток перед его запуском
            self.delay = 1  # TODO то устанавливайте значение 1

        while True:  # TODO Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # TODO с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # TODO с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # TODO с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # TODO с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    OK_STATUS = 200
    # TODO Пропишите сигналы, которые считаете нужными
    response = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__latitude: Optional[float] = None
        self.__longitude: Optional[float] = None
        self.__delay: Optional[int] = None
        self.__status: bool = False
        self.__api_url = ''

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        self.__longitude = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def api_url(self):
        return self.__api_url

    @api_url.setter
    def api_url(self, value: tuple):
        lat, lon = value
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&" \
                         f"longitude={lon}&current_weather=true"

    def run(self) -> None:
        # TODO настройте метод для корректной работы
        # print(f'\nlatitude = {self.latitude}, longitude = {self.longitude}, delay = {self.delay}')

        if not all([self.latitude, self.longitude]):
            print('Thread is closed\n')
            return

        self.status = True

        while self.status:

            try:
                # print(self.api_url)
                response = requests.get(self.api_url)

                if response.status_code != self.OK_STATUS:
                    print(f'Что-то пошло не так: status_code={response.status_code}')
                    self.status = False
                    return

                data = response.json()
                self.response.emit(data)
                time.sleep(self.delay)

            except Exception as e:
                print('harry')
                self.status = False
                print(e)
                return

