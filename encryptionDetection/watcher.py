from watchdog.observers import Observer
from .eventHandler import EncryptionCheckEventHandler
from .encryptDetect import EncryptionDetectionFactory

class  DirectoryWatcher:
    def __init__(self) -> None:
        self.observer = Observer()
        self.directory = "C:\\Users"
        pass   

    def initiateWatch(self):
        encryptionEventHandler = EncryptionCheckEventHandler(EncryptionDetectionFactory
                                                             .getEncryptionAlgorithm("shannon"))
        self.observer.schedule(encryptionEventHandler,self.directory,True)
        self.observer.start()

    def terminateWatch(self):
        self.observer.stop()
        self.observer.join()