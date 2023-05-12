from abc import ABC, abstractmethod


class Save(ABC):

    # абстрактный метод, который будет необходимо переопределять для каждого подкласса
    @abstractmethod
    def save_json(self):
        pass
