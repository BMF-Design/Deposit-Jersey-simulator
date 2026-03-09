class Timeline:
    def __init__(self):
        self.month = 1
        self.year = 1

    def advance(self, months: int = 1):
        self.month += months
        while self.month > 12:
            self.month -= 12
            self.year += 1

    def label(self) -> str:
        return f"Year {self.year} – Month {self.month}"