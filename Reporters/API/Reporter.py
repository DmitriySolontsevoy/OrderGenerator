import abc


class Reporter:
    @abc.abstractmethod
    def report(self):
        pass

    @abc.abstractmethod
    def __report_list(self, list, flavor_text):
        pass

    @abc.abstractmethod
    def __report_single_metric(self, metric, flavor_text):
        pass
