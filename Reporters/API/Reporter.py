import abc


class Reporter:
    stats = []

    @abc.abstractmethod
    def report(self):
        pass

    def fixate_time(self, start_time, finish_time, operation, amount):
        diff = (finish_time - start_time).total_seconds() * 1000
        self.stats.append("Time taken to " + operation + " (amount: " + str(amount) + "): " + str(diff) + " ms.")
