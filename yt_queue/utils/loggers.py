import sys

class StdLogger:
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

    def output(self, data):
        _stdout(data)

def _stdout(message):
    print(message)
def _stderr(message):
    print(message, file=sys.stderr)
