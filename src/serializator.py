class JobVacancy:
    '''класс для работы с вакансиями'''

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
        '''приводим полученну информацию в нужный вид'''
        return (f"{self.title}\n"
                f"{self.salary} - {self.currency}\n"
                f"{self.description}\n"
                # f"{self.description[:50]}...\n" if self.description is not None else "None"
                f"{self.link}\n")

    @classmethod
    def cast_object_list_to_dict(cls, job_list):
        return list(map(cls.serialize_obj_to_dict, job_list))

    @classmethod
    def serialize_obj_to_dict(cls, obj):
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

    @classmethod
    def show_vacancies(cls, vacancies_list):
        for vacancy in vacancies_list:
            print(vacancy)
