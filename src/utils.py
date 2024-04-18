import requests
import json
from abc import ABC, abstractmethod
from pprint import pprint


# абстрактный класс для работы с API сервиса с вакансиями
class JobAPI(ABC):
    baseurl = "https://api.hh.ru/"

    # def __init__(self):
    # self.params = {'text': '', 'page': 0, 'per_page': 100}

    @abstractmethod
    def get_vacancies(self):
        pass


# класс, наследующийся от абстрактного класса, для работы с платформой hh.ru
class HHJobAPI(JobAPI):

    def __init__(self):
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def get_vacancies(self, **kwargs):
        params = self.params.copy()
        params.update(kwargs)
        endpoint = "vacancies"
        url = self.baseurl + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # pprint(data)
            return data.get("items")
        else:
            return []


# a = HHJobAPI()
# a.get_vacancies()


# класс для работы с вакансиями
class JobVacancy:
    def __init__(self, title, link, salary, description, currency):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description
        self.currency = currency

        # валидация данных
        if not salary:
            self.salary = "Зарплата не указана"

    def __str__(self):
        return (f"{self.title} - {self.link}\n "
                f"{self.salary} - {self.currency}\n"
                f"{self.description}")

    @classmethod
    def cast_to_object_list(cls, job_list):
        return list(map(cls.json_serialize, job_list))

    @classmethod
    def json_serialize(cls, dict_job):
        pprint(dict_job)
        print(type(dict_job))
        pprint(dict_job.get("salary", {}))
        salary = dict_job.get("salary", {})
        currency = dict_job.get("salary", {}).get("currency")
        description = dict_job.get("snippet", {}).get("responsibility")

        return cls(
            title=dict_job.get("name"),
            link=dict_job.get("url"),
            salary=salary,
            currency=currency,
            description=description

        )


# абстрактный класс, который  реализует методы для добавления вакансий в файл,
# получения данных из файла по указанным критериям и удаления информации о вакансиях.
class JobFile(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(self, criteria):
        raise NotImplementedError

    @abstractmethod
    def delete_vacancy(self, vacancy):
        raise NotImplementedError


# класс для сохранения информации о вакансиях в JSON-файл
class JSONJobFile(JobFile):
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies(self, criteria):
        pass

    def delete_vacancy(self, vacancy):
        pass
