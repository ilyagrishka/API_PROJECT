def check_by_key_words(vacancy, filter_words):
    for word in filter_words:
        if word in vacancy.get('name') or vacancy.get('snippet').get('requirement'):
            return True


def filter_vacancies(vacancies, filter_words):
    return list(filter(lambda x: check_by_key_words(x, filter_words), vacancies))


def get_vacancies_by_salary(vacancies, salary_range):
    min_salary, max_salary = salary_range.split('-')
    filtered_vacancies = []
    for vacancy in vacancies:
        try:
            if vacancy['salary'] is not None:
                vacancy_salary = vacancy['salary']['from']
                if vacancy_salary is not None:
                    if int(min_salary) <= vacancy_salary <= int(max_salary):
                        filtered_vacancies.append(vacancy)
        except KeyError:
            continue
    return filtered_vacancies


def sort_vacancies(vacancies):
    return sorted(vacancies, key=lambda x: x['salary']['from'], reverse=True)


def get_top_vacancies(vacancies, n):
    return vacancies[:n]


def get_current_data(data, filter_words, salary_range, top_n):
    filtered_vacancies = filter_vacancies(data, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    return get_top_vacancies(sorted_vacancies, top_n)
