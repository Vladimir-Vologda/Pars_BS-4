#   Импорт требующихся библиотек
import csv
import requests
from bs4 import BeautifulSoup
from user_agent import user_a

URL = 'https://www.avito.ru/arhangelskaya_oblast/vakansii'
HOST = 'https://www.avito.ru'

#   HEADERS: для того, что бы requests выглядел как с браузера
HEADERS = {
    'User-Agent': f'{user_a()}',
    'Accept-Language': 'ru, en; q = 1',
}


#   Функция получения страници в HTML формате
def get_url(url):
    response = requests.get(url=url, headers=HEADERS)  # Запрос к URL и подставление нашего USER-AGENT
    return response.text  # Возвращение полученой страници в HTML формате


#   Разбор HTML
def get_parsing_html_and_write(html):
    lists = []  # Список для записи спарсиных данных
    soup = BeautifulSoup(html, 'lxml')

    #   Поиск всего что относится к этому тегу и классу (к первому найденному классу)
    all_block = soup.find('div', class_="items-items-kAJAg")

    #   Поиск всех отделов по этому тегу и классу в ALL_BLOCK
    one_block = all_block.find_all('div', class_="iva-item-content-rejJg")
    nam = 0

    with open("file.csv", mode="a", encoding='utf-8') as w_file:
        #   Прописываем названия полей
        names = ["Вакансия №", "Должность", "Зарплата", "Город", "Ссылка"]
        file_writer = csv.DictWriter(w_file, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writeheader()

        for el in one_block:  # Перебор всех найденных отделов ONE_BLOCK
            nam += 1

            #   Поиск названия должности
            try:
                title = el.find('div', class_="iva-item-titleStep-pdebR").text
            except Exception:
                title = f'No title'
            #   Поиск зарплаты
            price = el.find('div', class_="iva-item-priceStep-uq2CQ").text.replace('\xa0', ' ')

            #   Поиск ссылки
            try:
                links = el.find('div', class_="iva-item-titleStep-pdebR").find('a').get('href')
            except Exception:
                links = f'No links'
            # Поиск названия города
            try:
                city = el.find('div', class_="geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL").text
            except Exception:
                city = f'No city'

            #   Запись данных в поля
            file_writer.writerow({
                "Вакансия №": nam,
                "Должность": title,
                "Зарплата": price,
                "Город": city,
                "Ссылка": f'{HOST}{links}',
            })


#   Функция собирающая предыдущие
def main():
    url = URL
    html = get_url(url)    # 1-я функция, подстовляем наш url
    get_parsing_html_and_write(html)    # 2-я функция, подстовляем полученный предыдущей функцией html


#   Запуск функции
if __name__ == '__main__':
    main()

#   P.S.
#   Теги, Классы, ID и т.д. для каждого сайта индивидуальны
