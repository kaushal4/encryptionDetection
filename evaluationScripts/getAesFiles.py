import sys
from os import listdir
from os.path import isfile, join
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


testPath = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\kaushal.damania\\Documents\\encryptNotifier\\textFiles"
resultPath = sys.argv[2] if len(sys.argv) > 2 else "C:\\Users\\kaushal.damania\\Documents\\encryptNotifier\\aesTextFiles"
key = get_random_bytes(16)
print(key)

def getFilesInDir(directory:str) -> list[tuple[str,str]]:
    files_in_dir = [(f,join(directory, f))
                     for f in listdir(directory) if isfile(join(directory, f))]
    return files_in_dir

def getDirInDir(directory:str) -> list[tuple[str,str]]:
    dir_in_dir = [(f,join(directory,f)) for f in listdir(directory) if not isfile(join(directory, f))]
    return dir_in_dir


directories = getDirInDir(testPath)
decd = ""

for dir_name,dir in directories:
    files = getFilesInDir(dir)
    targetDir = join(resultPath,dir_name)
    for (fileName,filePath) in files:
        fin =  open(filePath, "rb")
        data = fin.read()
        fin.close()
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        targetFile = join(targetDir,fileName)
        fout =  open(targetFile,mode='wb')
        [fout.write(x) for x in (cipher.nonce, tag, ciphertext)]
        fout.close()