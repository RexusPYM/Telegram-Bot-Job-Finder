import requests
import pretty_errors
from bs4 import BeautifulSoup


class Parser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

    def get_data(self):
        pass

    def parse_data(self, data: str):
        pass

    def parse_tasks(self, tasks):
        pass

    def run(self):
        pass


class FreelanceRu(Parser):

    def __init__(self, request_text: str):
        super().__init__()
        self.url = f'https://freelance.ru/project/search/pro?c=&q={request_text}&m=or&e=&f=&t=&o=0&o=1'

    def get_data(self):
        response = self.session.get(url=self.url)
        return response.text

    def parse_data(self, data: str):
        soup = BeautifulSoup(data, 'lxml')
        tasks = soup.find_all('div', class_="box-shadow project")
        return self.parse_tasks(tasks=tasks)

    def parse_tasks(self, tasks):
        tasks_collection = []  # общий список заказов
        for task in tasks:  # цикл заполнения общего списка заказов
            lines = task.text.split('\n')
            lines = [line.strip() for line in lines if line]
            lines.insert(0, 'https://freelance.ru' + task.find('a', 'description')['href'])  # вставка ссылки на заказ

            tasks_collection.append(lines)

        return tasks_collection

    def run(self):
        data = self.get_data()
        return self.parse_data(data=data)


def main():
    freelanceru = FreelanceRu('')
    print(freelanceru.run())


if __name__ == '__main__':
    main()
