class TimePrinter:
    def __init__(self):
        self.secondsDisplayed: set = set()

    def printTime(self, time: int) -> None:
        if time not in self.secondsDisplayed:
            self.secondsDisplayed.add(time)
            print(f"Time left: {time}")

    def clear(self) -> None:
        self.secondsDisplayed.clear()


