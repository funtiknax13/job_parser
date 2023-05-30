import json
import os


from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class Save(ABC):
    """
    Абстрактный класс для работы с разными типами файлов,
    который позволяет добавлять вакансию в файл,
    получать вакансии по зарплате,
    удалять вакансию из файла
    """

    @abstractmethod
    def add_vacancy(self, vacancy: object):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary: str):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: object):
        pass


class SaveJSON(Save):
    file = "user_vacancies.json"
    save_file = os.path.join("data", file)

    def add_vacancy(self, vacancy: object) -> None:
        """
        Добавляет объект типа Vacancy в файл избранных вакансий
        """
        data = vacancy.to_dict()
        with open(self.save_file, "a", encoding="utf-8") as file:
            if os.stat(self.save_file).st_size == 0:
                json.dump([data], file)
            else:
                with open(self.save_file) as json_file:
                    data_list = json.load(json_file)
                data_list.append(data)
                with open(self.save_file, "w") as json_file:
                    json.dump(data_list, json_file)
        print(f"Вакансия добавлена в файл {self.save_file}")

    def get_vacancies_by_salary(self, salary: int):
        """
        Получает список вакансий по указанному уровню зарплаты
        """
        with open(self.save_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        select_result = []
        for item in data:
            if item["salary_from"] > salary or item["salary_to"] > salary:
                select_result.append(Vacancy.from_dict(item))
        return select_result

    def delete_vacancy(self, vacancy: object):
        """
        Удаляет указанную вакансию из файла
        """
        with open(self.save_file, "a", encoding="utf-8") as file:
            if os.stat(self.save_file).st_size != 0:
                with open(self.save_file) as json_file:
                    data_list = json.load(json_file)
                try:
                    data_list.remove(vacancy.to_dict())
                except ValueError:
                    print("Такой вакансии нет!")
                with open(self.save_file, "w") as json_file:
                    json.dump(data_list, json_file)
                    print("Вакансия удалена")


class Connection:
    """
    класс для работы с загруженными по апи вакансиями
    """

    def __init__(self, name: str) -> None:
        file = f"data_{name.title()}.json"
        self.save_file = os.path.join("data", file)

    def save(self, data: list) -> None:
        """Сохраняет загруженные вакансии в файл"""
        with open(self.save_file, "w", encoding="utf-8") as file:
            json.dump(data, file)
        print(f"Вакансии сохранены в файл {self.save_file}")

    def load(self):
        """Выгружает загруженные вакансии из файла"""
        try:
            with open(self.save_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("Файл с вакансиями не найден")

    def delete(self):
        """Удаляет файл с загруженными файлами"""
        if os.path.isfile(self.save_file):
            os.remove(self.save_file)
            print("Файл с вакансиями удалён")
        else:
            print("Файл с вакансиями не найден!")


