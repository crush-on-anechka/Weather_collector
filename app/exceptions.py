class RequestException(Exception):

    @classmethod
    def __str__(cls):
        return cls.__name__


class APIConnectionException(RequestException):
    pass


class BadResponseStatusException(RequestException):
    pass
