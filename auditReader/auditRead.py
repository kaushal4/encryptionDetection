import re
import subprocess
import queue
import datetime
from typing import List
from time import sleep
from auditItem import AuditItem

class AuditReader():
    __instance = None

    @staticmethod 
    def getInstance():
        if AuditReader.__instance == None:
            AuditReader()
        return AuditReader.__instance

    def __init__(self):
        self.__queue = queue.Queue()
        self.__lastAccessed = datetime.datetime.now()
        self.__terinate = False 
        self.__regex = r'pid=(\d+)\s.*?exe="(.*?)".*?key="(.*?)"'
        if AuditReader.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AuditReader.__instance = self

    def __readAudit(self) -> List[str]|None:
        cmd = "ausearch -k encryption -ts " + self.__lastAccessed.strftime("%Y-%m-%d %H:%M:%S")  
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        if(p.stdout !=  None):
            res = p.stdout.read().decode()
            reslines = res.splitlines()
            self.__lastAccessed = datetime.datetime.now()
            return reslines
        return None

    def __parseAudit(self,auditLine:str) -> AuditItem:
        matches = re.findall(self.__regex,auditLine)


    def __parseAuditLines(self,auditLines:List[str]) -> List[AuditItem]:
        res:List[AuditItem] = []
        for auditLine in auditLines:



    def start(self):
        while(not self.__terinate):
            sleep(1)
            self.__read_audit()


read_audit()
