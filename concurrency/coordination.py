## when two or more threads needs to kknow about an event or a change in the data strucutre. so that they can act on it. 
# for example producer and consumer problem. 

'''
task scheduler using blocking queue.

blocking queue gives all the efficient waiting on the queue for consumers. 
backpressure to not let more producers to produce more events. all at once. 
'''
from queue import Queue
from typing import Callable
class TaskScheduler:
    def __init__(self):
        self._queue: Queue[Callable[[], None]] = Queue(maxsize=1000) # always have a limit of the queue to not have OOM.

    def submit_task(self, task: Callable[[], None]) -> None:
        self._queue.put(task)

    def worker_loop(self) -> None:
        while True:
            task = self._queue.get() # blocked in queue is empty
            task()  # callable

'''
actor model of coordination

we have an actor in every process. each actor has a mailbox where messages can be dropped
the message once dropped can be picked up by the same thread and process

This is eliminating to have shared memory for coordinatin. the coordination is coming from 
message passing.
'''
from abc import ABC, abstractmethod

class Actor(ABC):
    def __init__(self):
        self._mailbox: Queue[str] = Queue()
        self.running = False
        self.thread = threading.Thread(target = self._run)
        self.thread.start()

    def _run(self):
        while self.running:
            try:
                message: str = self._mailbox.get(timeout = 0.1) # throws Empty error every 0.1 seconds
                self.on_receive(message)
            except self._mailbox.Empty:
                continue

    def send(self, message: str):
        self._mailbox.put(message)

    @abstractmethod
    def on_receive(self, message: str):
        pass
