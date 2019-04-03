import abc


class Reporter:
    @abc.abstractmethod
    def report(self):
        pass

    @abc.abstractmethod
    def report_list(self, list, flavor_text):
        pass
