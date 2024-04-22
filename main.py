from src.api_hh import HHJobAPI
from pprint import pprint
from src.file_storage import JSONJobFile
from src.utils import get_current_data
from src.serializator import JobVacancy


def user_interaction():
    hh_api = HHJobAPI()
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    vacancies = hh_api.get_vacancies(text=search_query)
    current_vacancies = get_current_data(vacancies, filter_words, salary_range, top_n)
    serialize_data = JobVacancy.cast_object_list_to_dict(current_vacancies)
    JobVacancy.show_vacancies(serialize_data)


if __name__ == "__main__":
    user_interaction()
