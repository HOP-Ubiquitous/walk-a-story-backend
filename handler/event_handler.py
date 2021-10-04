from threading import Thread

from handler.test_event import TestEvent


class EventHandler:

    def __init__(self):
        self.event_list = []

    def add_event(self, event):
        self.event_list.append(event)

    def run(self):
        for event in self.event_list:
            Thread(target=event.execute).start()


if __name__ == '__main__':
    eh = EventHandler()
    eh.add_event(TestEvent('datos'))
    eh.run()
