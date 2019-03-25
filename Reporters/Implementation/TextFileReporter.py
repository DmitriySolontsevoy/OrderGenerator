from Reporters.API.Reporter import Reporter
from Services.Logger.Implementation.TextFileLogger import TextFileLogger


class TextFileReporter(Reporter):
    def __init__(self, path):
        self.path = path

    def report(self):
        TextFileLogger.info("Attempting to open file for report writing: " + self.path)

        try:
            file = open(self.path, "a")
            for item in self.stats:
                file.write(item + '\n')
        except OSError:
            TextFileLogger.warn("Couldn't open file for writing report!")
