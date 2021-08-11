"""Copyright 2021, James S. Wang, All rights reserved."""


class TimePrinter:
    """A helper class used to print a timer countdown.

    Attributes:
        secondsDisplayed (set): A set of seconds that have already been
            displayed. Makes it so that multiple calls to printTime() will only
            print each second once.
    """

    def __init__(self):
        self.secondsDisplayed: set = set()

    def printTime(self, time: int) -> None:
        """Prints the time in seconds, ensuring no duplicates.

        Args:
            time (int): The time in seconds to print.
        """
        if time not in self.secondsDisplayed:
            self.secondsDisplayed.add(time)
            print(f"Time left: {time}")

    def clear(self) -> None:
        """Resets the cache of seconds that have already been printed."""
        self.secondsDisplayed.clear()
