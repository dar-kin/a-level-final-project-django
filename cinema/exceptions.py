class SessionsCollideException(Exception):
    pass


class IncorrectDataRangeException(Exception):
    pass


class IncorrectDataException(Exception):
    pass


class NoFreePlacesException(Exception):
    pass


class BookedSessionExistsException(Exception):
    pass


class DateExpiredException(Exception):
    pass


class NotEnoughMoneyException(Exception):
    pass