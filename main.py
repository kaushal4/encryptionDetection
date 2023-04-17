import time
import tracemalloc
from psutil import cpu_count,Process
import os
from encryptionDetection.watcher import DirectoryWatcher


def main():
    p = Process(os.getpid())
    tracemalloc.start()
    directoryWatcher:DirectoryWatcher = DirectoryWatcher()
    directoryWatcher.initiateWatch()
    try:
        while True:
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage is {current / 10**3}KB")
            print(f"Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
            print(f"Cpu percentage is {p.cpu_percent()/cpu_count()}")
            time.sleep(4)

    except KeyboardInterrupt:
        directoryWatcher.terminateWatch()
    tracemalloc.stop()

if __name__ == "__main__":
    main()