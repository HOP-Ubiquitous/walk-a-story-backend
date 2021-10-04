class TestEvent:
    def __init__(self, data):
        self.data = data

    def execute(self):
        print(self.data)
