import random
from common.exceptions import UrlDomainTooShort, InvalidUrl
from common.regex_rules import URL_FIRST_DOMAIN_PATTERN, URL_HOME_PAGE_PATTERN


def get_homepage(url: str) -> str:
    home_page = URL_HOME_PAGE_PATTERN.match(url)
    if home_page is None:
        raise InvalidUrl(url)
    return home_page.group(0)


def get_domain(url: str) -> str:
    domain = URL_FIRST_DOMAIN_PATTERN.match(url)
    if domain is None:
        raise InvalidUrl(url)
    return domain.group(2)


def shorten_url(url: str) -> str:
    domain = get_domain(url)[:5]

    if len(domain) < 2:
        raise UrlDomainTooShort(url, domain)

    if len(domain) == 2:
        new_url = domain[0] + '.' + domain[1]
    else:
        new_url = domain[:-2] + '.' + domain[-2:]

    return new_url + '/' + generate_url_id(length=4)


def generate_url_id(*, length):
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    row_id = random.choices(symbols, k=length)
    return ''.join(row_id)


