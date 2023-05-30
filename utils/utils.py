from src.vacancy import Vacancy
from src.api import SuperJobAPI, HeadHunterAPI
from src.save import SaveJSON, Connection


def load_vacancies(job: str) -> list:
    """Функция для загрузки вакансий с двух ресурсов
    по указанному ключевому слову

    :param job: ключевое слово для поиска вакансий
    :return: список вакансий
    """
    hh_api = HeadHunterAPI()
    hh_api.get_vacancies(job)
    vacancies = hh_api.get_formatted_vacancies()
    sj_api = SuperJobAPI()
    sj_api.get_vacancies(job)
    vacancies.extend(sj_api.get_formatted_vacancies())
    print(f"Загружено {len(vacancies)} вакансий")
    return vacancies


def get_vacancies(data: list) -> list:
    """
    :param data: список вакнсий в формате списка словарей
    :return: возвращает список вакнсий в формате экземпляров класса
    """
    vacancies = []
    for item in data:
        vacancy = Vacancy.from_dict(item)
        vacancies.append(vacancy)
    return vacancies


def print_vacancies(data: list) -> None:
    """
    :param data: получает список вакансий в формате экземпляров класса
    печатает список вакансий на экран
    """
    vacancy_index = 1
    for vacancy in data:
        print(vacancy_index, vacancy)
        print("_" * 20)
        vacancy_index += 1


def sort_vacancies(data: list) -> list:
    """

    :param data: получает список вакансий в формате экземпляров класса
    :return: возвращает список вакансий отсортированный по максимально указанной зарплате
    """
    result = sorted(data, reverse=True)
    print("Вакансии отсортированы по зарплате")
    return result


def filter_vacancies(data: list, salary: int) -> list:
    """

    :param data: список вакансий в формате экземпляров класса
    :param salary: зарплата для фильтрации
    :return: список вакансий с зарплатой выше указанной
    """
    result = []
    for vacancy in data:
        if vacancy.get_salary() >= salary:
            result.append(vacancy)
    print("Вакансии отфильтрованы по зарплате")
    return result

