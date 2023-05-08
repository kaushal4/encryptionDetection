from psutil import cpu_count,Process
import time
import tracemalloc

class Metrices:
    def __init__(self,process: Process):
        self.process = process

    def printMetrices(self):
        tracemalloc.start()
        try:
            while True:
                current, peak = tracemalloc.get_traced_memory()
                print(f"Current memory usage is {current / 10**3}KB")
                print(f"Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
                print(f"Cpu percentage is {self.process.cpu_percent()/cpu_count()}")
                time.sleep(4)

        except KeyboardInterrupt:
            tracemalloc.stop()
