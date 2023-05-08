import threading
import time
from .processTracer import ProcessTracer
from .processEvaluator import ProcessEvaluator


class EvaluationController():
    def __init__(self, pid: int,minEncryptionWrites: int = 0):
        self.__pe: ProcessEvaluator = ProcessEvaluator(pid,minEncryptionWrites)
        self.__tracer: ProcessTracer = ProcessTracer(self.__pe)

    def run(self):
        thread = threading.Thread(target=self.__tracer.run,group=None)
        thread.start()  
        while (thread.is_alive()):
            time.sleep(1)
            self.__pe.evaluate()
        self.__tracer.Terminate()
    
    def Terminate(self):
        self.__tracer.Terminate()