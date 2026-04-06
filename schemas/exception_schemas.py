class UserAlreadyExist(Exception):
    pass


class UserDidntExist(Exception):
    pass


class ErrorWithJWT(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidUserType(Exception):
    pass


class RoomNotFound(Exception):
    pass


class DatesNotFound(Exception):
    pass

class DatesBlockError(Exception):
    pass