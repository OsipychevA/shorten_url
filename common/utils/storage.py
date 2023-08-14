import os.path
import json


class Storage:
    def __init__(self, shorts: dict[str, str] | None = None,
                 pseudonyms: dict[str, str] | None = None) -> None:
        self.__shorts: dict[str, str] = shorts or dict()
        self.__pseudonyms: dict[str, str] = pseudonyms or dict()

    @property
    def shorts(self) -> dict[str, str]:
        return self.__shorts.copy()

    @property
    def pseudonyms(self) -> dict[str, str]:
        return self.__pseudonyms.copy()

    def add_short_url(self, short_url: str, url: str) -> None:
        self.__shorts[short_url] = url

    def add_pseudonym(self, pseudonym: str, homepage_url: str) -> None:
        self.__pseudonyms[pseudonym] = homepage_url

    def has_short(self, short_url: str) -> bool:
        return short_url in self.__shorts

    def has_pseudonym(self, pseudonym: str) -> bool:
        return pseudonym in self.__pseudonyms

    def get_homepage_url(self, pseudonym: str) -> str:
        return self.__pseudonyms[pseudonym]

    def get_full_url(self, short: str) -> str:
        return self.__shorts[short]


def save_data_to_json(storage: Storage, file_path: str) -> None:
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump({'shorts': storage.shorts, 'pseudonyms': storage.pseudonyms}, file, ensure_ascii=False)


def load_data_from_json(file_path: str) -> Storage:
    if not os.path.exists(file_path):
        return Storage()
    with open(file_path, mode='r', encoding='utf-8') as file:
        data: dict[str, dict[str, str]] = json.load(file)
    return Storage(**data)
