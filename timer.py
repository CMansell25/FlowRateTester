import time

class Timer:
    def __init__(self):
        self.start_time = None
 
    def start(self):
        self.start_time = time.time()

    def stop(self):
        pass
 
    def get_time_ms(self):
        if self.start_time is None:
            raise ValueError("Timer has not been started yet.")
        elapsed_time = time.time() - self.start_time
        return int(elapsed_time * 1000)
 