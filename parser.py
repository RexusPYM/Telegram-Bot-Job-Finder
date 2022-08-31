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

    def parse_block(self, block):
        pass

    def run(self):
        pass


class FreelanceRu(Parser):

    url = 'https://freelance.ru/project/search/pro'

    def get_data(self):
        response = self.session.get(url=self.url)
        return response.text

    def parse_data(self, data: str):
        soup = BeautifulSoup(data, 'lxml')
        tasks = soup.find_all('div', class_="box-shadow project highlight")
        self.parse_tasks(tasks=tasks)

    def parse_tasks(self, tasks):
        print('=' * 150)
        for task in tasks:
            lines = task.text.split('\n')

            # while '' in lines:
            #     lines.remove('')

            for line in lines:
                if line != '':
                    print(line.strip())

            # print(task.text.strip())
            print('=' * 150)

    def run(self):
        data = self.get_data()
        self.parse_data(data=data)


def main():
    freelanceru = FreelanceRu()
    freelanceru.run()


if __name__ == '__main__':
    main()
