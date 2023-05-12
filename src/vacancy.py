import requests
import json
from abc import ABC, abstractmethod


class JobFindAPI(ABC):

    @abstractmethod
    def get_vacancies(self, name: str) -> list:
        pass


class HeadHunterAPI(JobFindAPI):

    def get_vacancies(self, name: str) -> list:
        params = {
            'text': name,  # Имя вакансии для поиска
            # 'area': 1,  # Расположение вакансии (1 -  Москва)
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        req = requests.get("https://api.hh.ru/vacancies", params)
        data = json.loads(req.content.decode())
        vacancies = []
        for item in data["items"][0:7]:
            name = item["name"]
            area = item["area"]["name"]
            experience = item["experience"]["name"]
            link = "https://hh.ru/vacancy/" + item["id"]
            vacancy = Vacancy(name, area, link)
            vacancies.append(vacancy)

        # test = data["items"][5]
        # print(test)
        # id = test["id"]
        # name = test["name"]
        # area = test["area"]["name"]
        # experience = test["experience"]["name"]
        # link = "https://hh.ru/vacancy/" + test["id"]
        # salary = test["salary"]
        # print(f"Вакансия: {name}\nРасположение: {area}\nТребуемый опыт: {experience}\nСсылка: {link}")
        # if salary:
        #     salary_from = test["salary"]["from"]
        #     salary_to = test["salary"]["to"]
        #     salary_cur = test["salary"]["currency"]
        #     print(f"Зарплата: от {salary_from} до {salary_to} {salary_cur}")
        # else:
        #     print("Зарплата: не указана")
        #     salary_from = 0
        #     salary_from = 0
        return vacancies


class SuperJobAPI(JobFindAPI):

    def get_vacancies(self, name: str) -> list:
        pass


class Vacancy:

    def __init__(self, name: str, area: str, link: str) -> None:
        self.name = name
        self.area = area
        self.link = link

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.area}, {self.link})"


hh_api = HeadHunterAPI()
vacancies = hh_api.get_vacancies("Python")
# print(repr(vacancies[0]))
# for vacancy in vacancies:
#     print(vacancy.name, vacancy.area, vacancy.link, sep="\t")
