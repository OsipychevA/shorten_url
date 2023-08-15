
import logging
from json import JSONDecodeError

from common import exceptions, messages
from common.settings import DATA_FILE_PATH, LOG_FILE_PATH
from common.utils.regex import shorten_url, get_domain, get_homepage
from common.utils.storage import load_data_from_json, Storage, save_data_to_json
from common.utils.url_request import get_response_code_url


def main():
    """Function that launches the application"""
    config_logging()

    try:
        storage = load_data_from_json(DATA_FILE_PATH)
    except JSONDecodeError as e:
        logging.critical(str(e), stack_info=True)
        print(messages.JSON_FILE_ERROR.format(DATA_FILE_PATH))
        return

    run_app = True
    while run_app:
        run_app = choice_options(storage)


def config_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format='%(asctime)s, %(levelname)s, %(filename)s, Message: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.INFO,
    )


def choice_options(storage: Storage):
    logging.info('The "choise_options" function is running')
    selection_options = {
        1: (messages.MENU_REDUCE_URL, reduce_url, True),
        2: (messages.MENU_GET_HOMEPAGE_BY_PSEUDONYM, get_homepage_by_pseudonym, True),
        3: (messages.MENU_GET_FULL_URL_BY_SHORT, get_full_url_by_short, True),
        4: (messages.MENU_GET_ALL_DATA, get_all_data, True),
        5: (messages.MENU_STOP_APP, stop_app, False),
    }

    print()
    print(messages.MENU_LABEL)
    for key, value in selection_options.items():
        print(f'{key} - {value[0]}')

    choice = int(input('\n' + messages.MENU_CHOICE_INPUT))
    if choice in selection_options:
        selection_options[choice][1](storage)
        return selection_options[choice][2]

    else:
        print(messages.MENU_CHOICE_ERROR)
        return True


def reduce_url(storage: Storage):
    logging.info('The "reduce_url" function is running')
    url = input(messages.REGISTER_URL_INPUT)
    try:
        pseudonym = get_domain(url)
        home_page = get_homepage(url)
    except exceptions.InvalidUrl as e:
        logging.info(str(e))
        print(messages.INVALID_URL_ERROR)
        return

    try:
        short_url = shorten_url(url)
    except exceptions.UrlDomainTooShort as e:
        logging.info(str(e))
        print(messages.DOMAIN_TOO_SHORT_ERROR)
        return
    storage.add_pseudonym(pseudonym, home_page)
    storage.add_short_url(short_url, url)
    print(messages.SHORT_URL_OUTPUT.format(short_url))
    print(messages.PSEUDONYM_OUTPUT.format(pseudonym))
    print(messages.URL_OUTPUT.format(url))


def get_homepage_by_pseudonym(storage: Storage):
    logging.info('The "get_homepage_by_pseudonym" function is running')
    pseudonym = input(messages.PSEUDONYM_INPUT)
    if storage.has_pseudonym(pseudonym):
        home_page = storage.get_homepage_url(pseudonym)
        response_code = get_response_code_url(home_page)
        print(messages.URL_OUTPUT.format(home_page))
        print(messages.PSEUDONYM_OUTPUT.format(pseudonym))
        print(messages.RESPONSE_CODE_OUTPUT.format(response_code))
        logging.info('Data successfully found')
    else:
        print(messages.PSEUDONYM_NOT_FOUND)
        logging.info('Pseudonym not found')


def get_full_url_by_short(storage: Storage):
    logging.info('The "get_full_url_by_short" function is running')
    short_url = input(messages.SHORT_URL_INPUT)
    if storage.has_short(short_url):
        full_url = storage.get_full_url(short_url)
        response_code = get_response_code_url(full_url)
        print(messages.URL_OUTPUT.format(full_url))
        print(messages.SHORT_URL_OUTPUT.format(short_url))
        print(messages.RESPONSE_CODE_OUTPUT.format(response_code))
        logging.info('Data successfully found')
    else:
        print(messages.SHORT_URL_NOT_FOUND)
        logging.info('Short url not found')


def get_all_data(storage: Storage):
    logging.info('The "get_all_data" function is running')
    print(messages.PSEUDONYM_LIST_LABEL)
    for item in storage.pseudonyms.items():
        print(item)
    print()
    print(messages.SHORT_URL_LIST_LABEL)
    for item in storage.shorts.items():
        print(item)


def stop_app(storage: Storage):
    print(messages.STOP_APP)
    logging.info('Stop app and save file to database')
    save_data_to_json(storage, DATA_FILE_PATH)
    logging.info('File with data successfully save to database')


if __name__ == '__main__':
    main()