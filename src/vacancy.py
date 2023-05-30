class Vacancy:
    """Класс Вакансия содержит атрибуты:
        имя вакансии
        старт зарплаты
        потолок зарплаты
        валюта зарплаты
        требуемый опыт
        ссылка на вакансию
    """

    def __init__(self, name: str, link: str,
                 salary_from: int, salary_to: int,
                 salary_cur: str, experience: str) -> None:
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_cur = salary_cur
        self.experience = experience
        self.link = link

    @classmethod
    def from_dict(cls, item: dict):
        """
        Формирует экземпляр класса из словаря
        """
        return cls(item["name"], item["link"], item["salary_from"],
                   item["salary_to"], item["salary_currency"], item["experience"])

    def to_dict(self):
        """
         Формирует словарь из экземпляра класса
         """
        return {"name": self.name,
                "link": self.link,
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
                "salary_currency": self.salary_cur,
                "experience": self.experience}

    def __str__(self):
        return f"{self.name} ({self.link})\n" \
               f"{self.salary_from}-{self.salary_to} {self.salary_cur}\n" \
               f"Требования: {self.experience}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}," \
               f" {self.link}, {self.salary_from}, {self.salary_to}," \
               f" {self.salary_cur}, {self.experience})"

    def get_salary(self):
        """Выводит максимальную зарплату указанную работодателем"""
        return max(self.salary_from, self.salary_to)

    def __lt__(self, other):
        return int(self.get_salary()) < int(other.get_salary())

    def __gt__(self, other):
        return int(self.get_salary()) > int(other.get_salary())

    def __le__(self, other):
        return int(self.get_salary()) <= int(other.get_salary())

    def __ge__(self, other):
        return int(self.get_salary()) >= int(other.get_salary())

    def __eq__(self, other):
        return int(self.get_salary()) == int(other.get_salary())
