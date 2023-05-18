from .accessType import AccessType

class AuditItem():
    def __init__(self,fileName:str,pid:str,type:AccessType) -> None:
        self.fileName = fileName
        self.pid = pid 
        self.AccessType = AccessType


