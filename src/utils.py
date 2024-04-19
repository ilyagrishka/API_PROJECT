import requests
import json
from abc import ABC, abstractmethod
from pprint import pprint
import os


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
        self.encoding = 'UTF-8'

    def get_vacancies(self, **kwargs):
        params = self.params.copy()
        params.update(kwargs)
        endpoint = "vacancies"
        url = self.baseurl + endpoint
        response = requests.get(url, params=params)
        response.encoding = self.encoding
        if response.status_code == 200:
            data = response.json()
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

    def __repr__(self):
        return (f"{self.title} - {self.link}\n"
                f"{self.salary} - {self.currency}\n"
                f"{self.description[:50]}...\n" if self.description is not None else "None")

    @classmethod
    def cast_object_list_to_dict(cls, job_list):
        return list(map(cls.serialize_obj_to_doct, job_list))

    @classmethod
    def serialize_obj_to_doct(cls, obj):
        return obj.__dict__

    @classmethod
    def cast_object_list_from_file(cls, job_list):
        return list(map(cls.serialize_dict_to_obj, job_list))

    @classmethod
    def serialize_dict_to_obj(cls, dict_job):
        return cls(
            title=dict_job.get("name"),
            link=dict_job.get("url"),
            salary=dict_job.get('salary'),
            currency=dict_job.get('currency'),
            description=dict_job.get('description')

        )

    @classmethod
    def cast_to_object_list(cls, job_list):
        return list(map(cls.json_serialize, job_list))

    @classmethod
    def json_serialize(cls, dict_job):
        salary = dict_job.get("salary")
        if salary:
            amount = salary.get("from")
            currency = salary.get("currency")
        else:
            amount = None
            currency = None

        description = dict_job.get("snippet", {}).get("responsibility")

        return cls(
            title=dict_job.get("name"),
            link=dict_job.get("url"),
            salary=amount,
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

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError


# класс для сохранения информации о вакансиях в JSON-файл
class JSONJobFile(JobFile):
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            with open(filename, "r", encoding="UTF-8") as file:
                data = json.load(file)
                self.data = JobVacancy.cast_object_list_from_file(data)
        self.data = []

    def add_vacancy(self, vacancy):
        if isinstance(vacancy, list):
            self.data.extend(vacancy)
        elif isinstance(vacancy, JobVacancy):
            self.data.append(vacancy)

    def get_vacancies(self, **criteria):
        object_list = []
        for k, v in criteria.items():
            filtered_object = list(filter(lambda x: getattr(x, k) == v, self.data))
            object_list.extend(filtered_object)
        return object_list

    def delete_vacancy(self, vacancy):
        self.data.remove(vacancy)

    def get_all(self):
        return self.data.copy()

    def commit(self):
        with open(self.filename, "w", encoding="UTF-8") as file:
            json.dump(JobVacancy.cast_object_list_to_dict(self.data), file)
