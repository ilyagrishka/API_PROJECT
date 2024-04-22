import json
from abc import ABC, abstractmethod
import os
from src.serializator import JobVacancy


class JobFile(ABC):
    '''абстрактный класс, который  реализует методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.'''

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


class JSONJobFile(JobFile):
    '''класс для сохранения информации о вакансиях в JSON-файл'''

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
