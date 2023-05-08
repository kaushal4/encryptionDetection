import datetime

# TODO: make this a non static class


class MeasureTime():
    start = datetime.datetime.now()

    @staticmethod
    def start():
        MeasureTime.start = datetime.datetime.now()

    @staticmethod
    def getTime() -> float:
        return (datetime.datetime.now() - MeasureTime.start).total_seconds()
