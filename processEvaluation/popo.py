import enum


class OperationType(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    CREATE = "CREATE"


class ProcessOperation():

    def __init__(
            self,
            operationType: OperationType,
            filePath: str,
            contents: str) -> None:
        self.operationType = operationType
        self.filePath = filePath
        self.contents: str = contents
