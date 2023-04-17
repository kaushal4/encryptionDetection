from datetime import datetime, timedelta
from watchdog.events import FileSystemEventHandler; 
from watchdog.events import FileModifiedEvent; 
from .encryptDetect import EncryptionDetectionInterface;

class EncryptionCheckEventHandler(FileSystemEventHandler) :

    def __init__(self,encryption_detection:EncryptionDetectionInterface) -> None:
        super().__init__()
        self.last_modified = datetime.now()
        self.encryption_detection = encryption_detection
        self.write_trigger_gap = 1

    def __isMultiTrigger(self,time_in_seconds:int) -> bool:
        if datetime.now() - self.last_modified < timedelta(seconds=time_in_seconds):
            return True
        else:
            self.last_modified = datetime.now()
            return False
    
    def __evaluateEncryption(self,srcPath) -> bool :
        byte_array:list[bytes] = []
        with open(srcPath, "rb") as fin:
            # reading first 1000 bytes
            count = 1000
            while((byte := fin.read(1)) and count):
                byte_array.append(byte)
                count-=1
            fin.close()
        return self.encryption_detection.DetectFromByteArray(byte_array)

    def on_modified(self, event):
        # this below is to prevent multiple modified operations
        # being triggered for the same action
        if self.__isMultiTrigger(self.write_trigger_gap):
            return
        if type(event) is FileModifiedEvent:
            src_path = event.src_path
            print("Modification detected")
            if(self.__evaluateEncryption(src_path)):
                print("encryption action taken on file " + src_path)
