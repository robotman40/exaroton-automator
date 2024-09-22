import time

class TimeTracker:
    def __init__(self, ):
        self.start_time = time.time()
        
    def get_time_elapsed(self):
        return (int(time.time() - self.start_time))/60