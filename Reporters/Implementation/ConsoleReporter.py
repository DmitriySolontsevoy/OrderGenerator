from Reporters.API.Reporter import Reporter
from Services.Logger.Implementation.Logging import Logging
from ReportData.ReportData import ReportData


class ConsoleReporter(Reporter):
    def report(self):
        Logging.info("Started console reporting")
        self.report_list(ReportData.generated_red, "Red zone generation")
        self.report_list(ReportData.generated_green, "Green zone generation")
        self.report_list(ReportData.generated_blue, "Blue zone generation")

        self.report_list(ReportData.messaged_red, "Red zone RMQ messaging")
        self.report_list(ReportData.messaged_green, "Green zone RMQ messaging")
        self.report_list(ReportData.messaged_blue, "Blue zone RMQ messaging")

        self.report_list(ReportData.written_red, "Red zone file writing")
        self.report_list(ReportData.written_green, "Green zone file writing")
        self.report_list(ReportData.written_blue, "Blue zone file writing")

        self.report_list(ReportData.read_red, "Red zone file reading")
        self.report_list(ReportData.read_green, "Green zone file reading")
        self.report_list(ReportData.read_blue, "Blue zone file reading")

        self.report_list(ReportData.inserted_red, "Red zone DB insertion")
        self.report_list(ReportData.inserted_green, "Green zone DB insertion")
        self.report_list(ReportData.inserted_blue, "Blue zone DB insertion")

    def report_list(self, list, flavor_text):
        if len(list) > 0:
            amount = len(list)
            s = sum(list)
            minimum = min(list)
            maximum = max(list)
            average = s/amount
            print("{} (amount = {}):\nMin: {} ms\nMax: {} ms\nAvg: {} ms\n".format(flavor_text, amount, minimum,
                                                                                   maximum, average))
