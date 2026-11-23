import time

class CircuitBreaker:
    """Stops calling a friend that keeps failing. After a rest, it lets one call try again."""

    def __init__(self, failure: int = 5, reset_seconds: float = 10):
        self.failures = failure
        self.rest_seconds = reset_seconds
        self.count = 0
        self.opened_at: float | None = None

    @property
    def state(self) -> str:
        if self.opened_at is None:
            return "CLOSED"
        if time.time() - self.opened_at > self.rest_seconds:
            return "HALF-OPEN"
        return "OPEN"

    def allow(self) -> bool:
        return self.state != "OPEN"

    def success(self):
        self.count = 0
        self.opened_at = None

    def failure(self):
        self.count += 1
        if self.count >= self.failures:
            self.opened_at = time.time()


Breaker = CircuitBreaker