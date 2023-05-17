import enum
import queue
import re
import subprocess
import time
from typing import Dict

from utils import measeTimeUtils

from .popo import OperationType, ProcessOperation
from .processEvaluator import ProcessEvaluator


class ProcessSyscallType(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    OPEN = "OPEN"
    CREATE = "CREATE"


class ProcessSyscall():

    def __init__(self, pst: ProcessSyscallType, data: str) -> None:
        self.pst: ProcessSyscallType = pst
        self.data: str = data


class straceStartFail(Exception):
    def __init__(self):
        self.message = "Failed to start trace, or start trace not called"


class ProcessTracer():

    OPEN_OPERATIONS = ["open", "openat"]
    READ_OPERATIONS = ["read"]
    WRITE_OPERATIONS = ["write"]
    SAVE_OPERATIONS = ["create"]
    OPEN_REGEX = r'\w+\(.*?"(.+)",.*?\) = (\d+)'
    READ_REGEX = r'read\(\s*(\d+)\s*,\s*"([^"]*)"\s*,?\s*(.+)?\)\s*=\s*\d+'
    WRITE_REGEX = r'write\(\s*(\d+)\s*,\s*"([^"]*)"\s*,?\s*(.+)?\)\s*=\s*\d+'
    CREATE_REGEX = r'mmap\(.*?, \d+, .*, .*, (?P<fd>\d+), .*'

    def __init__(self, pe: ProcessEvaluator) -> None:
        # Queue of Process Operation
        self.__operations: queue.Queue = queue.Queue()
        self.__straceProcess: subprocess.Popen | None = None
        self.fileMap: Dict[int, str] = {}
        self.pe = pe
        self.straceCommand = [
            'strace', '-p', str(pe.pid), '-e', "trace=file,read,write",
            "-s", str("65535"),'-o', './processEvaluation/output.txt']

    def __startTrace(self) -> None:
        self.__straceProcess = subprocess.Popen(self.straceCommand, stdout=subprocess.PIPE)
        measeTimeUtils.MeasureTime.start()

    def Terminate(self) -> None:
        if self.__straceProcess is not None:
            self.__straceProcess.terminate()

    def isQueueEmpty(self) -> bool:
        return self.__operations.empty()

    def __parseOpenOperation(self, straceOutput: str) -> None:
        match = re.match(self.OPEN_REGEX, straceOutput)
        if match:
            filepath: str = match.group(1)
            fileDescriptor: int = int(match.group(2))
            self.fileMap[fileDescriptor] = filepath

    def __parseReadOperation(
            self,
            straceOutput: str) -> ProcessOperation | None:
        match = re.match(self.READ_REGEX, straceOutput)
        if match:
            fileDescriptor: int = int(match.group(1))
            data: str = str(match.group(2))
            return ProcessOperation(
                OperationType.READ, self.fileMap[fileDescriptor], data)
        print(f"Failed to parse read operation \n {straceOutput} \n {self.READ_REGEX}")
        return None

    def __cleanWriteContent(self, content: str) -> str:
        cleanedContent = re.sub(r'\\x[0-9A-Fa-f]{0,1}$', '', content)

        # replace incomplete backslashes
        cleanedContent = re.sub(r'\\{1}$', '', content)
        return content

    def __parseWriteOperation(
            self,
            straceOutput: str) -> ProcessOperation | None:
        match = re.match(self.WRITE_REGEX, self.__cleanWriteContent(straceOutput))
        if match:
            fileDescriptor: int = int(match.group(1))
            data: str = str(match.group(2))
            if(fileDescriptor in self.fileMap):
                return ProcessOperation(
                    OperationType.WRITE, self.fileMap[fileDescriptor], data)
        print(f"Failed to parse write operation \n {straceOutput} \n {self.WRITE_REGEX}")
        return None

    def __parseCreateOperation(
            self,
            straceOutput: str) -> ProcessOperation | None:
        match = re.match(self.CREATE_REGEX, straceOutput)
        if match:
            fileDescriptor: int = int(match.group("fd"))
            return ProcessOperation(
                OperationType.CREATE, self.fileMap[fileDescriptor], "")
        return None

    def __parseOperation(self, straceOutput: str):
        sysCall = self.__getOperation(straceOutput)
        if (sysCall == ProcessSyscallType.OPEN):
            self.__parseOpenOperation(straceOutput)
        elif (sysCall == ProcessSyscallType.READ):
            processOperation = self.__parseReadOperation(straceOutput)
            if (processOperation is not None):
                # self.__operations.put(processOperation)
                self.pe.handleOperation(processOperation)
        elif (sysCall == ProcessSyscallType.WRITE):
            processOperation = self.__parseWriteOperation(straceOutput)
            if (processOperation is not None):
                # self.__operations.put(processOperation)
                self.pe.handleOperation(processOperation)
        elif (sysCall == ProcessSyscallType.CREATE):
            processOperation = self.__parseCreateOperation(straceOutput)
            if (processOperation is not None):
                # self.__operations.put(processOperation)
                self.pe.handleOperation(processOperation)

    def __getOperation(self, straceOutput: str) -> ProcessSyscallType | None:
        operation = straceOutput.split('(')[0]
        if (operation.casefold() in self.OPEN_OPERATIONS):
            return ProcessSyscallType.OPEN
        elif (operation.casefold() in self.READ_OPERATIONS):
            return ProcessSyscallType.READ
        elif (operation.casefold() in self.WRITE_OPERATIONS):
            return ProcessSyscallType.WRITE
        else:
            return None

    def popQueue(self) -> ProcessOperation:
        return self.__operations.get()

    def run(self) -> None:
        self.__startTrace()
        if (self.__straceProcess is not None):
            with open('./processEvaluation/output.txt', 'r') as f:
                while True:
                    command = f.readline()
                    if (len(command) != 0):
                        self.__parseOperation(
                            str(command))
                    time.sleep(0.1)
            self.__straceProcess.wait()
        raise straceStartFail()