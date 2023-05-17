import datetime

# TODO: make this a non static class


class MeasureTime():
    __startTime = datetime.datetime.now()
    __hasStarted = False

    @staticmethod
    def start():
        if (MeasureTime.__hasStarted):
            return
        MeasureTime.__startTime = datetime.datetime.now()
        MeasureTime.__hasStarted = True

    @staticmethod
    def getTime() -> float:
        return (datetime.datetime.now() - MeasureTime.__startTime).total_seconds()
