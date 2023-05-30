import requests
import json
import os

from abc import ABC, abstractmethod


class JobFindAPI(ABC):
    """абстрактный класс для получения и форматирования списка вакансий"""
    @abstractmethod
    def get_vacancies(self, name: str) -> list:
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass


class HeadHunterAPI(JobFindAPI):
    """
    Класс для работы с api HeadHunter
    """
    api_link = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.data = []
        self.vacancies = []

    def get_vacancies(self, name: str) -> list:
        """Получает список вакансий по ключевому слову name с HH"""
        for page_index in range(10):
            params = {
                'text': name,  # Имя вакансии для поиска
                'page': page_index,  # Индекс страницы поиска на HH
                'per_page': 100  # Кол-во вакансий на 1 странице
            }
            try:
                response = requests.get(self.api_link, params)
                response_data = json.loads(response.content.decode())["items"]
                self.data.extend(response_data)
                print("Загружено 100 вакансий (HeadHunter)")
            except Exception as ex:
                break
        return self.data

    def get_formatted_vacancies(self):
        """
        Форматирует полученнный список вакансий
        в формат словаря с заданными полями
        """
        self.vacancies = []
        for item in self.data:
            name = item["name"]
            experience = item["experience"]["name"]
            link = "https://hh.ru/vacancy/" + item["id"]
            salary = item["salary"]
            if salary:
                salary_from = item["salary"]["from"]
                if not salary_from:
                    salary_from = 0
                salary_to = item["salary"]["to"]
                if not salary_to:
                    salary_to = 0
                salary_cur = item["salary"]["currency"].lower()
                if salary_cur == "rur":
                    salary_cur = "rub"
            else:
                salary_from = 0
                salary_to = 0
                salary_cur = "rub"
            vacancy = {"name": name,
                       "link": link,
                       "salary_from": salary_from,
                       "salary_to": salary_to,
                       "salary_currency": salary_cur,
                       "experience": experience}
            self.vacancies.append(vacancy)
        return self.vacancies


class SuperJobAPI(JobFindAPI):
    """
    Класс для работы с api SuperJob
    """

    SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
    api_link = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self):
        self.data = []
        self.vacancies = []

    def get_vacancies(self, name: str) -> list:
        """Получает список вакансий по ключевому слову name с SuperJob"""
        headers = {'X-Api-App-Id': self.SUPERJOB_API_KEY}
        for page_index in range(10):
            params = {"page": page_index,
                      "count": 100,
                      "keyword": name}
            response = requests.get(self.api_link,
                                        params=params, headers=headers)
            response_data = json.loads(response.content.decode())["objects"]
            if len(response_data) != 0:
                print("Загружено 100 вакансий (SuperJob)")
                self.data.extend(response_data)
            else:
                break
        return self.data

    def get_formatted_vacancies(self):
        """
        Форматирует полученнный список вакансий
        в формат словаря с заданными полями
        """
        self.vacancies = []
        for item in self.data:
            name = item["profession"]
            salary_from = item["payment_from"]
            salary_to = item["payment_to"]
            salary_cur = item["currency"].lower()
            experience = item["experience"]["title"]
            link = item["link"]
            vacancy = {"name": name,
                       "link": link,
                       "salary_from": salary_from,
                       "salary_to": salary_to,
                       "salary_currency": salary_cur,
                       "experience": experience}
            self.vacancies.append(vacancy)

        return self.vacancies

