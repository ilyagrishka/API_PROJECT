from src.utils import HHJobAPI, JobVacancy, JSONJobFile
from pprint import pprint


# Создание экземпляра класса для работы с API сайтов с вакансиями

# hh_api = HHJobAPI()
#
# # Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.get_vacancies(text="Python")
#
# # Преобразование набора данных из JSON в список объектов
# vacancies_list = JobVacancy.cast_to_object_list(hh_vacancies)
# file = JSONJobFile("test.json")
# file.add_vacancy(vacancies_list)
# print(file.get_all())
# file.commit()


# Пример работы контструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
#
# # Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)

# # функция для взаимодействия с пользователем
# def interact_with_user():
#
#
#
# # Main

def check_by_key_words(vacancy, filter_words):
    for word in filter_words:
        if word in vacancy.get('name') or vacancy.get('snippet').get('requirement'):
            return True
        else:
            False


def filter_vacancies(vacancies, filter_words):
    pprint(vacancies)
    return list(filter(lambda x: check_by_key_words(x, filter_words), vacancies))


def get_vacancies_by_salary(vacancies, salary_range):
    min_salary, max_salary = salary_range.split('-')
    filtered_vacancies = []
    for vacancy in vacancies:
        try:
            vacancy_salary = vacancy['salary']['from']
            if min_salary < vacancy_salary < max_salary:
                filtered_vacancies.append(vacancy)
        except KeyError:
            continue
    return filtered_vacancies


def sort_vacancies(vacancies):
    return sorted(vacancies, key=lambda x: x['salary']['from'], reverse=True)


def get_top_vacancies(vacancies, n):
    return vacancies[:n]


def user_interaction():
    hh_api = HHJobAPI()
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    vacancies = hh_api.get_vacancies(text=search_query)

    filtered_vacancies = filter_vacancies(vacancies, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    pprint(top_vacancies)


if __name__ == "__main__":
    user_interaction()
