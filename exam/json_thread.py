import json
import time
from datetime import datetime

from PySide6 import QtCore


class JsonThread(QtCore.QThread):
    # In seconds.
    HOURS = 3600
    MINUTES = 60

    signal = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._delay = 1
        self._status = None

    @property
    def delay(self):
        return self._delay

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def run(self):
        self.status = True

        while self.status:
            current_date = datetime.now().strftime('%d.%m.%Y %H:%M')  # str
            current_date = datetime.strptime(current_date, '%d.%m.%Y %H:%M')  # object

            try:
                notes_dict = self.load_json()

                for key, value in notes_dict.items():
                    expiry_date = value['expiry_date']  # '19.06.2023 22:43'
                    expiry_date = datetime.strptime(expiry_date, '%d.%m.%Y %H:%M')  # object

                    delta = expiry_date - current_date  # datetime.timedelta(days=9, seconds=3600)
                    days = delta.days
                    hours = delta.seconds // JsonThread.HOURS
                    minutes = (delta.seconds // JsonThread.MINUTES) % JsonThread.MINUTES

                    time_to_expiry = (key, days, hours, minutes)
                    self.signal.emit(time_to_expiry)

            except FileNotFoundError as err:
                pass

            time.sleep(self.delay)

    @staticmethod
    def load_json():
        with open('my_notes', 'r') as json_file:
            notes_dict = json.load(json_file)

        return notes_dict

    @staticmethod
    def save_json(notes_dict):
        with open('my_notes', 'w') as json_file:
            json.dump(notes_dict, json_file, indent=4, ensure_ascii=False)
