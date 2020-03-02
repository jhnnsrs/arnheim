class StatusCode(object):
    STARTED = 2000
    DONE = 1000
    PROGRESS = 3000
    ERROR = 4000


class Messages(object):
    STARTED = "Starting"
    ERROR = "Error"
    PROGRESS = "Progress"
    DONE = "Done"

    @staticmethod
    def error(message) -> str:
        return Messages.ERROR + " - " + str(message)

    @staticmethod
    def progress(percent) -> str:
        return Messages.PROGRESS + " - " + str(percent)


class LarvikStatus(object):

    def __init__(self,code: int, message: str = None):
        self.statuscode = code
        self.message = message if message is not None else ""


def larvikError(message = None):
    return LarvikStatus(StatusCode.ERROR,message)


def larvikProgress(message = None):
    return LarvikStatus(StatusCode.PROGRESS,message)


def larvikDone(message = None):
    return LarvikStatus(StatusCode.DONE,message)