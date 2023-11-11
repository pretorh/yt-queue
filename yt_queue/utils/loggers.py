import sys

class NoOpLogger:
    def info(self, message):
        pass
    def warning(self, message):
        pass
    def error(self, message):
        pass
    def output(self, data):
        pass

class QuietLogger(NoOpLogger):
    def output(self, data):
        _stdout(data)

class StdLogger(QuietLogger):
    def __init__(self, formatted_output=False):
        self.formatted_output = formatted_output

    def info(self, message):
        if self.formatted_output:
            _stderr(message)
        else:
            _stdout(message)

    def warning(self, message):
        _stderr(message)

    def error(self, message):
        _stderr(message)

def _stdout(message):
    print(message)
def _stderr(message):
    print(message, file=sys.stderr)
