from utils.utils import get_vacancies, load_vacancies, sort_vacancies, print_vacancies, filter_vacancies
from src.save import Connection, SaveJSON
from time import sleep


def user_interaction():
    """
    Пользовательский интерфейс, позволяющий
    загрузить список вакансий по ключевому слову
    вывести N вакансий на экран (указывает пользователь)
        вывести новые N вакансий
        сохранить вакансию в избранное
    отсортировать список вакансий по зарплате
    отфильтровать список вакансий по уровню зарплаты указанной пользователем
    удалить файл с вакансиями по ключевому слову
    загрузить файл с выбранными вакансиями
        удалить вакансию из избранных
    выйти из программы
    """
    vacancies = []
    user_query = ""
    while True:
        print("Загрузить вакансии - 1, Вывести вакансии - 2,",
              "Отсортировать по зарплате - 3, Отфильтровать по зарплате - 4,",
              "Удалить загруженные вакансии - 5,",
              "Загрузить избранные - 6, Выйти - 7")
        user_choice = input()
        if user_choice == "2":
            print("Введите количество вакансий для отображения:")
            top_n = int(input())
            if len(vacancies) < top_n:
                print_vacancies(vacancies)
            else:
                start = 0
                print_vacancies(vacancies[start:start + top_n])
                while True:
                    print(f"Следующие {top_n} вакансий - 1, Сохранить вакансию - 2, Выйти - 3")
                    user_choice = input()
                    if user_choice == "3":
                        break
                    elif user_choice == "2":
                        user_vacancy = int(input(f"Укажите номер вакансии для сохранения (1 - {top_n})"))
                        vacancy = vacancies[start+user_vacancy]
                        saver = SaveJSON()
                        saver.add_vacancy(vacancy)
                    else:
                        start += top_n
                        print_vacancies(vacancies[start:start + top_n])
        elif user_choice == "3":
            vacancies = sort_vacancies(vacancies)
        elif user_choice == "7":
            break
        elif user_choice == "5":
            connect = Connection(user_query)
            connect.delete()
        elif user_choice == "6":
            loader = SaveJSON()
            while True:
                vacancies = loader.get_vacancies_by_salary(0)
                print_vacancies(vacancies)
                print("Удалить вакансию - 1, Отмена - 2")
                user_answer = input()
                if user_answer == "1":
                    print(f"Укажите номер вакансии 1 - {len(vacancies)}")
                    user_vacancy_number = int(input())
                    if 0 < user_vacancy_number < len(vacancies):
                        loader.delete_vacancy(vacancies[user_vacancy_number-1])
                    else:
                        print("Вы указали неправильный номер вакансии.")
                        sleep(2)
                else:
                    break

        elif user_choice == "4":
            user_filter = int(input("Укажите минимальный высший уровень зарплаты:"))
            vacancies = filter_vacancies(vacancies, user_filter)
        else:
            print("Введите ключевое слово для поиска вакансий: ")
            user_query = input()
            vacancies = load_vacancies(user_query)
            connect = Connection(user_query)
            connect.save(vacancies)
            vacancies = get_vacancies(vacancies)


if __name__ == '__main__':
    user_interaction()
