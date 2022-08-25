from threading import Condition

class MultiQueue:
    def __init__(self):
        self.queue = bytearray()
        self.cv = Condition()
        self.finished = False
        self.bytes_needed = 0

    def mark_finished(self):
        self.finished = True
        self.cv.notify_all()

    def is_finished(self):
        return self.finished

    def extend(self, data):
        with self.cv:
            self.queue.extend(data)
            if len(self.queue) > self.bytes_needed:
                self.cv.notify()

    def read(self, num_bytes):
        with self.cv:
            while len(self.queue) < num_bytes or self.is_finished():
                self.cv.wait()

            # if we are notified because we are finished, just return the rest of the bytes
            if self.is_finished():
                return self.queue
            bytes = self.queue[:num_bytes]
            self.queue = self.queue[num_bytes:]
            return bytes






