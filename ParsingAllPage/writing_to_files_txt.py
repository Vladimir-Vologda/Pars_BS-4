#   Импорт требующихся библиотек
from time import sleep

import requests
from bs4 import BeautifulSoup

from user_agent import user_a


#   Если вы собираетесь спарсить много страниц без подмены PROXY либо временного промежутка,
#   то сервер выдаст 429 ошибку.
#   Ошибка 429 означает, что пользователь посылает слишком много запросов
#   за короткий временной промежуток.

URL = 'https://www.avito.ru/arhangelskaya_oblast/vakansii'
HOST = 'https://www.avito.ru'

#   HEADERS: для того, что бы requests выглядел как с браузера
HEADERS = {
    'UserAgent': f'{user_a()}',
    'Accept-Language': 'ru, en; q = 0.9',
}


#   Функция получения страници в HTML формате
def get_url(url):
    response = requests.get(url=url, headers=HEADERS)  # Запрос к URL и подставление нашего USER-AGENT
    # print(response.status_code)
    return response.text  # Возвращение полученой страници в HTML формате


#   Определение количества страниц
def get_all_page(html):
    soup = BeautifulSoup(html, 'lxml')
    #   блок страниц
    num_all_page = soup.find('div', class_="js-pages pagination-pagination-_FSNE")
    #   кнопка "Следующая страница"
    num_last = num_all_page.find('span', class_="pagination-item-JJq_j pagination-item_arrow-Sttbt")
    #   просмотр идущего перед num_last тэга
    num = num_last.find_previous()
    return num.text


nam = 0


#   Разбор HTML
def get_parsing_html(html):
    lists = []  # Список для записи спарсиных данных
    soup = BeautifulSoup(html, 'lxml')

    #   Поиск всего что относится к этому тегу и классу (к первому найденному классу)
    all_block = soup.find('div', class_="items-items-kAJAg")

    #   Поиск всех отделов по этому тегу и классу в ALL_BLOCK
    one_block = all_block.find_all('div', class_="iva-item-content-rejJg")

    for el in one_block:  # Перебор всех найденных отделов ONE_BLOCK
        global nam
        nam += 1

        #   Поиск названия должности
        try:
            title = el.find('div', class_="iva-item-titleStep-pdebR").text
        except Exception:
            title = f'No vacancy'

        #   Поиск зарплаты
        try:
            price = el.find('div', class_="iva-item-priceStep-uq2CQ").text.replace('\xa0', ' ')
        except Exception:
            price = f'No price'

        #   Поиск ссылки
        try:
            links = el.find('div', class_="iva-item-titleStep-pdebR").find('a').get('href')
        except Exception:
            links = f'No link'

        # Поиск названия города
        try:
            city = el.find('div', class_="geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL").text
        except Exception:
            city = f'No city'

        lists.append(
            f'Вакансия №{nam}\n'
            f'Должность: {title}\n'
            f'Зарплата: {price}\n'
            f'Город: {city}\n'
            f'Ссылка: {HOST}{links}\n\n\''
        )  # Запись всех найденных элементов в список (способом добавления)
    return lists  # Возвращение полученного списка


#   Функция записи в TXT формат
def writer(data):
    with open('file.txt', 'a') as file:
        file.writelines(data)


#   Функция собирающая предыдущие
def main():
    url = URL
    html = get_url(url)    # 1-я функция, подстовляем наш url
    number = get_all_page(html)
    num = int(number)
    for i in range(1, num+1):
        #   Sleep: замарозка процесса на указанное количество секунд,
        #   таким образом, каждый запрос к серверу будет разделён определённым количеством временеи,
        #   токой метод долгий, но не нуждается в PROXY.
        sleep(10)
        url = f'{URL}?p={i}'
        html = f'{get_url(url)}'
        data = get_parsing_html(html)    # 2-я функция, подстовляем полученный предыдущей функцией html
        writer(data)    # 3-я функция, записываем полученный предыдущей функцией результат в TXT формат
        print(url)


#   Запуск функции
if __name__ == '__main__':
    main()

#   P.S.
#   Теги, Классы, ID и т.д. для каждого сайта индивидуальны
