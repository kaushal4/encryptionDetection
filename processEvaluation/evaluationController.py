import threading
from .processTracer import ProcessTracer
from .processEvaluator import ProcessEvaluator


class EvaluationController():
    def __init__(self, pid: int,minEncryptionWrites: int = 0):
        self.__pe: ProcessEvaluator = ProcessEvaluator(pid,minEncryptionWrites)
        self.__tracer: ProcessTracer = ProcessTracer(self.__pe)

    def run(self):
        tracerThread = threading.Thread(target=self.__tracer.run,group=None)
        tracerThread.start()  
        while (tracerThread.is_alive()):
            if(self.__pe.evaluate()):
                break
        self.Terminate()    

    def Terminate(self):
        self.__tracer.Terminate()