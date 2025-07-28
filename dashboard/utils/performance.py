import time

class PerformanceMonitor:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def elapsed(self):
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time