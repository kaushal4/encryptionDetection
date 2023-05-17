import os
import random
import string
from time import sleep
from typing import List

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

RANDOM_STRING = "Life is full of good things, including love and relationships, health and well-being, learning and personal growth, nature and beauty, and creativity and self-expression, among many others. Ultimately, what brings joy and fulfillment to one person may differ from another, but it's important to identify and pursue the things that bring meaning to your own life."

KEY = get_random_bytes(16)
readContent: dict[str, str] = {}

filesRead = 0
filesWritten = 0
encryptedFilesWritten = 0


def getContantToWrite() -> str:
    if (len(readContent) == 0):
        return RANDOM_STRING
    random_key = random.choice(list(readContent.keys()))
    random_value = readContent[random_key]
    del readContent[random_key]
    return random_value


def encrptedWrite(filePath: str, content: str):
    i: int = 1
    with open(filePath, 'wb') as randomfile:
        cipher = AES.new(KEY, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(
            content.encode('utf-8'))
        [randomfile.write(x) for x in (cipher.nonce, tag, ciphertext)]


def printFilesReadAndWritten():
    print("files read: " + str(filesRead), " files Written: " + str(filesWritten),
          " encrypted files written: " + str(encryptedFilesWritten))


def listFiles(startpath) -> List[str]:
    res = []
    for root, _, files in os.walk(startpath):
        for file in files:
            res.append(os.path.join(root, file))
    return res


def getRandomFileName(extension: str) -> str:
    letters = string.ascii_lowercase
    # generates a random 10-character string
    file_name = ''.join(random.choice(letters) for i in range(10))
    return file_name + extension


def pickRandomAndRead(filepathlist: list[str]):
    if (len(filepathlist) == 0):
        print("filelist is empty please provide a non empty file list")
        return
    randomfilepath = filepathlist[random.randint(0, len(filepathlist) - 1)]
    with open(randomfilepath, 'r') as randomfile:
        readContent[randomfilepath] = randomfile.read()
        global filesRead
        filesRead += 1
    printFilesReadAndWritten()


def pickRandomAndWrite(filepathlist: list[str]):
    if (len(filepathlist) == 0):
        print("filelist is empty please provide a non empty file list")
        return
    randomfilepath = filepathlist[random.randint(0, len(filepathlist) - 1)]
    encrptedWrite(randomfilepath, getContantToWrite())
    global filesWritten
    global encryptedFilesWritten
    filesWritten += 1
    encryptedFilesWritten += 1


def createRandomAndWrite(dirToWrite: str):
    if (len(readContent) == 0):
        return
    if (len(dirToWrite) == 0 and os.path.exists(dirToWrite) and os.path.isdir(dirToWrite)):
        print("incorrect directory to write")
        return
    randomfilepath = os.path.join(dirToWrite, getRandomFileName(".txt"))
    encrptedWrite(randomfilepath, getContantToWrite())
    global filesWritten
    global encryptedFilesWritten
    filesWritten += 1
    encryptedFilesWritten += 1
    printFilesReadAndWritten()


def runRandomReadWrite(seconds: int, readDir: str, writeDir: str):
    filePathsInDirRead = listFiles(readDir)
    isWrite = False
    try:
        while (True):
            if (isWrite):
                createRandomAndWrite(writeDir)
            else:
                pickRandomAndRead(filePathsInDirRead)
            sleep(seconds)
            isWrite = not isWrite
    except KeyboardInterrupt:
        print("exiting")


print(os.getpid())
sleep(10)
runRandomReadWrite(5, "/home/kaushal/Documents/abroad/encrypting/testDir/readDir",
                   "/home/kaushal/Documents/abroad/encrypting/testDir/writeDir")