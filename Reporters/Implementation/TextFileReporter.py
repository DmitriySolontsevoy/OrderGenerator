from Reporters.API.Reporter import Reporter
from Services.Logger.Implementation.Logging import Logging
from ReportData.ReportData import ReportData


class TextFileReporter(Reporter):
    def __init__(self, path, file_service, db_service):
        self.path = path
        self.file_service = file_service
        self.file = None
        self.db_service = db_service

    def report(self):
        Logging.info("Attempting to open file for report writing: " + self.path)
        self.file = self.file_service.open_file(self.path, "w")
        self.__report_list(ReportData.generated_red, "Red zone generation")
        self.__report_list(ReportData.generated_green, "Green zone generation")
        self.__report_list(ReportData.generated_blue, "Blue zone generation")

        self.__report_list(ReportData.messaged_red, "Red zone RMQ messaging")
        self.__report_list(ReportData.messaged_green, "Green zone RMQ messaging")
        self.__report_list(ReportData.messaged_blue, "Blue zone RMQ messaging")

        self.__report_single_metric(ReportData.received_from_rabbit, "Amount of messages received from RMQ")

        result = self.db_service.select("""SELECT count(*) FROM mytable UNION
            SELECT count(DISTINCT id) FROM mytable UNION
            SELECT count(*) FROM (SELECT * FROM mytable GROUP BY id HAVING count(*) = 2 AND status = 2) AS T UNION
            SELECT count(*) FROM (SELECT count(*) FROM mytable GROUP BY id HAVING count(*) = 3) AS T UNION
            SELECT count(*) FROM (SELECT * FROM mytable GROUP BY id HAVING count(*) = 2 AND status = 1) AS T;""")
        self.__report_single_metric(int(result[0][0]), "Amount of records in the database")
        self.__report_single_metric(result[1][0], "Amount of orders in the database")
        self.__report_single_metric(result[2][0], "Orders in red zone")
        self.__report_single_metric(result[3][0], "Orders in green zone")
        self.__report_single_metric(result[4][0], "Orders in blue zone")

    def __report_list(self, list, flavor_text):
        if len(list) > 0:
            amount = len(list)
            minimum = min(list)
            maximum = max(list)
            average = sum(list)/amount
            self.file_service.write_line(self.file, "{} (amount = {}):\nMin: {} ms\nMax: {} ms\nAvg: {} ms\n"
                                         .format(flavor_text, amount, minimum, maximum, average))

    def __report_single_metric(self, metric, flavor_text):
        self.file_service.write_line(self.file, "{}: {}\n".format(flavor_text, metric))
