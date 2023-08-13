import re


URL_FIRST_DOMAIN_PATTERN = re.compile(r'http[s]?://(.*\.)?(.+)\.')  # https://www.aviasales.org -> aviasales
URL_HOME_PAGE_PATTERN = re.compile(r'http[s]?://[^/]+')  # https://www.aviasales.org/?query=dsfsd -> https://www.aviasales.org
