import requests
from abc import ABC, abstractmethod


class JobAPI(ABC):
    ''' абстрактный класс для работы с API сервиса с вакансиями'''

    baseurl = "https://api.hh.ru/"

    @abstractmethod
    def get_vacancies(self):
        pass


class HHJobAPI(JobAPI):
    '''класс, наследующийся от абстрактного класса, для работы с платформой hh.ru'''

    def __init__(self):
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.encoding = 'UTF-8'

    def get_vacancies(self, **kwargs):
        '''получаем вакансии с сайта'''

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
