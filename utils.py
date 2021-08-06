from cogbattle import CogBattle


class TimePrinter:
    def __init__(self):
        self.secondsDisplayed = set()

    def printTime(self, time):
        if time not in self.secondsDisplayed:
            self.secondsDisplayed.add(time)
            print(f"Time left: {time}")

    def clear(self):
        self.secondsDisplayed.clear()


