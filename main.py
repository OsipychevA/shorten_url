from common import exceptions
from common.settings import DATA_FILE_PATH
from common.utils.regex import shorten_url, get_domain, get_homepage
from common.utils.storage import load_data_from_json, Storage, save_data_to_json
from common.utils.url_request import get_response_code_url


def main():
    """Function that launches the application"""
    storage = load_data_from_json(DATA_FILE_PATH)

    run_app = True
    while run_app:
        run_app = choice_options(storage)


def choice_options(storage: Storage):
    selection_options = {
        1: ('регистрация короткого интернет-адреса по стандартному', reduce_url, True),
        2: ('получение и проверка домашней страницы интернет-адреса по псевдониму', get_homepage_by_pseudonym, True),
        3: ('получение и проверка стандартного интернет-адреса по короткому', get_full_url_by_short, True),
        4: ('получение всех пар адресов', get_all_data, True),
        5: ('завершение программы', stop_app, False),
    }

    print('\nВведите')
    for key, value in selection_options.items():
        print(f'{key} - {value[0]}')

    choice = int(input('\nВаш выбор: '))
    if choice in selection_options:
        selection_options[choice][1](storage)
        return selection_options[choice][2]

    else:
        print('Введите значение от 1 до 5')
        return True


def reduce_url(storage: Storage):
    url = input('Введите стандартный url для регистрации: ')
    try:
        pseudonym = get_domain(url)
        home_page = get_homepage(url)
    except exceptions.InvalidUrl as e:
        print('Неверный URL. URL должен начинаться на https:// и должен содержать домены нулевого и первого уровней\n'
              '(прим. https://www.aviasales.org)')
        return
    try:
        short_url = shorten_url(url)
    except exceptions.UrlDomainTooShort as e:
        print('Неверный URL. Домен должен быть длиннее 1 символа\n'
              '(прим. https://www.aviasales.org)')
        return
    storage.add_pseudonym(pseudonym, home_page)
    storage.add_short_url(short_url, url)
    print(f'Короткий интернет адрес: {short_url}')
    print(f'Псевдоним домашней страницы: {pseudonym}')
    print(f'Стандартный интернет-адрес: {url}')


def get_homepage_by_pseudonym(storage: Storage):
    pseudonym = input('Введите псевдоним домашней страницы url: ')
    if storage.has_pseudonym(pseudonym):
        home_page = storage.get_homepage_url(pseudonym)
        response_code = get_response_code_url(home_page)
        print(f'Стандартный интернет-адрес: {home_page}')
        print(f'Псевдоним домашней страницы интернет-адрес: {pseudonym}')
        print(f'Код ответа страницы: {response_code}')
    else:
        print('Страница с таким псевдонимом не найдена')


def get_full_url_by_short(storage: Storage):
    short_url = input('Введите сокращенный url: ')
    if storage.has_short(short_url):
        full_url = storage.get_full_url(short_url)
        response_code = get_response_code_url(full_url)
        print(f'Стандартный интернет-адрес: {full_url}')
        print(f'Короткий интернет-адрес: {short_url}')
        print(f'Код ответа страницы: {response_code}')
    else:
        print('Страница не найдена')


def get_all_data(storage: Storage):
    print('Псевдонимы:')
    for item in storage.pseudonyms.items():
        print(item)
    print('\nКороткие интернет-адреса:')
    for item in storage.shorts.items():
        print(item)


def stop_app(storage: Storage):
    print('Завершение работы программы')
    save_data_to_json(storage, DATA_FILE_PATH)


if __name__ == '__main__':
    main()