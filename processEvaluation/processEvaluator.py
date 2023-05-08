import time

from utils import measeTimeUtils
from .popo import ProcessOperation, OperationType
from detectionAlorithms import isEncrypted
import struct
import re


class ProcessEvaluator():
    def __init__(self, pid: int, minimumEncryptionWrite: int, shouldBackup: bool = False) -> None:
        self.pid = pid
        self.shouldBackup = shouldBackup
        self.__filesCreated = 0
        self.__createdFileList: set[str] = set()
        self.__encryptionWrites = 0
        self.__encryptionModifies = 0
        self.__reads = 0
        self.__writes = 0
        self.__backup: dict[str, str] = {}
        self.__encryptionModifiesLen = 0
        self.__encryptionWritesLen = 0
        self.__WriteLen = 0
        self.__readFiles: set[str] = set()
        self.__encryptionModifiesFiles: set[str] = set()
        self.__encryptionWritesFiles: set[str] = set()
        self.__writeFiles: set[str] = set()
        self.__minEWrite = minimumEncryptionWrite

    def __handleReadOperation(self, operation: ProcessOperation) -> None:
        if (operation.filePath not in self.__readFiles):
            self.__readFiles.add(operation.filePath)
            self.__reads += 1
        # TODO handle backups

    def __getByteArray(self, operation: ProcessOperation):
        # replace incomplete byte sequences
        input_str = re.sub(r'\\x[0-9A-Fa-f]{0,1}$', '', operation.contents)

        # replace incomplete backslashes
        input_str = re.sub(r'\\{1}$', '', input_str)
        bytes_list = input_str.encode().decode('unicode_escape').encode('latin1')
        # Decode the byte string as UTF-8
        byte_list = [bytes([b]) for b in bytes_list]
        return byte_list

    def __handleWriteOperation(self, operation: ProcessOperation) -> None:
        if isEncrypted(self.__getByteArray(operation)):
            if (operation.filePath in self.__createdFileList):
                if (operation.filePath not in self.__encryptionModifiesFiles):
                    self.__encryptionModifiesFiles.add(operation.filePath)
                    self.__encryptionModifies += 1
                self.__encryptionModifiesLen += len(operation.contents)
            else:
                if (operation.filePath not in self.__encryptionWritesFiles):
                    self.__encryptionWritesFiles.add(operation.filePath)
                    self.__encryptionWrites += 1
                self.__encryptionWritesLen += len(operation.contents)
        if (operation.filePath not in self.__writeFiles):
            self.__writeFiles.add(operation.filePath)
            self.__writes += 1
        self.__WriteLen += len(operation.contents)

    def __handleCreateOperation(self, operation: ProcessOperation) -> None:
        self.__filesCreated += 1
        self.__createdFileList.add(operation.filePath)

    def handleOperation(self, operation: ProcessOperation) -> None:
        if (operation.operationType == OperationType.READ):
            self.__handleReadOperation(operation)
        if (operation.operationType == OperationType.WRITE):
            self.__handleWriteOperation(operation)
        if (operation.operationType == OperationType.CREATE):
            self.__handleCreateOperation(operation)

    def evaluate(self):
        print(f"read: {self.__reads} \n\
                ewrites: {self.__encryptionWrites} \n\
                emodifies = {self.__encryptionModifies} \n\
                writes = {self.__writes} \n\
                created = {self.__filesCreated}")
        if (self.__reads <= 0 or self.__WriteLen <= 0):
            return
        eWrites = self.__encryptionWrites + self.__encryptionModifies
        eWriteRatio = eWrites / self.__reads
        eEncryptionOutputRatio = self.__encryptionModifiesLen + \
            self.__encryptionWritesLen / self.__WriteLen
        if (eWrites > self.__minEWrite
                and (eWriteRatio > 0.5 or eEncryptionOutputRatio > 0.5)):
            print("encryption detected with pid" + self.pid)
            print(f"Time taken  to find: {measeTimeUtils.MeasureTime.getTime()}")
