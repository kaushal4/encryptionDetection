import sys
from os import listdir
from os.path import isfile, join
from encryptionDetection.encryptDetect import  EncryptionDetectionShanonEntropy

testPath = sys.argv[1] if len(sys.argv) > 1 else ".\\aesTextFiles"

def getFilesInDir(directory:str) -> list[str]:
    files_in_dir = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    return files_in_dir

def getDirInDir(directory:str) -> list[str]:
    dir_in_dir = [join(directory, f) for f in listdir(directory) if not isfile(join(directory, f))]
    return dir_in_dir

directories = getDirInDir(testPath)

files = []
for dir in directories:
    files.extend(getFilesInDir(dir)) 


def evaluateEncryption(srcPath) -> bool :
    byte_array:list[bytes] = []
    with open(srcPath, "rb") as f:
        # reading first 1000 bytes
        count = 1000
        while((byte := f.read(1)) and count):
            byte_array.append(byte)
            count-=1
    return EncryptionDetectionShanonEntropy.DetectFromByteArray(byte_array)

encryptCount = 0
normalCount = 0

for file in files:
    if evaluateEncryption(file):
        encryptCount+=1
    else:
        normalCount+=1

print("result :\n encrypted : " + str(encryptCount) + " \n not encrypted : " + str(normalCount))
