class Stopwatch:
    
    def __init__(self, startTime):
        self.lastEventTime = startTime

    def update(self, time):
        return time - self.lastEventTime

    def reset(self, time):
        self.lastEventTime = time