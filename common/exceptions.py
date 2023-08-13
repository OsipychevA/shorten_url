
class ApplicationException(BaseException):
    pass


class UrlDomainTooShort(ApplicationException):
    def __init__(self, url: str, domain: str) -> None:
        self.url = url
        self.domain = domain
        super().__init__(f'Url "{self.url}" has too short first-level domain "{self.domain}"')


class InvalidUrl(ApplicationException):
    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__(f'Url "{self.url}" is invalid')