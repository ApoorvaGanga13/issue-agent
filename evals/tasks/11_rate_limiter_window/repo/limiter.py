class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.calls = []

    def allow(self, now):
        if len(self.calls) < self.limit:
            self.calls.append(now)
            return True
        return False
