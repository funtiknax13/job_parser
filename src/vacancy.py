import requests
import json
from abc import ABC, abstractmethod
from keys import SuperJobAPIKey


class JobFindAPI(ABC):

    @abstractmethod
    def get_vacancies(self, name: str) -> list:
        pass


class HeadHunterAPI(JobFindAPI):

    def get_vacancies(self, name: str) -> list:
        params = {
            'text': name,  # Имя вакансии для поиска
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        response = requests.get("https://api.hh.ru/vacancies", params)
        data = json.loads(response.content.decode())
        vacancies = []
        for item in data["items"]:
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
            salary = f"{salary_from}-{salary_to} {salary_cur}"
            vacancy = {
                "name": name,
                "link": link,
                "salary": salary,
                "experience": experience

            }
            vacancies.append(vacancy)
        return vacancies


class SuperJobAPI(JobFindAPI):

    # SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
    SUPERJOB_API_KEY = SuperJobAPIKey

    def get_vacancies(self, name: str) -> list:
        headers = {'X-Api-App-Id': self.SUPERJOB_API_KEY}
        vacancies_count = 100
        params = {'count': vacancies_count,
                  'keyword': name}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                    params=params, headers=headers)
        data = json.loads(response.content.decode())
        vacancies = []
        for item in data["objects"]:
            name = item["profession"]
            salary_from = item["payment_from"]
            salary_to = item["payment_to"]
            salary_cur = item["currency"].lower()
            experience = item["experience"]["title"]
            link = item["link"]
            salary = f"{salary_from}-{salary_to} {salary_cur}"
            vacancy = {
                "name": name,
                "link": link,
                "salary": salary,
                "experience": experience
            }
            vacancies.append(vacancy)

        return vacancies


class Vacancy:

    def __init__(self, name: str, salary: str, experience: str, link: str) -> None:
        self.name = name
        self.salary = salary
        self.experience = experience
        self.link = link

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.link}, {self.salary}, {self.experience})"


hh_api = HeadHunterAPI()
vacancies = hh_api.get_vacancies("Python")
sj_api = SuperJobAPI()
vacancies.extend(sj_api.get_vacancies("Python"))
for vacancy in vacancies:
    print(vacancy)
print(len(vacancies))