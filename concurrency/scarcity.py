"""
think of database connection pool. we have a pool of 10 connection to handle the incoming
1000 requests, what happens if all the 10 connections are hung due to some error in the code or large sql queries. 

This is called scarcity problem.
"""

# we can create a semaphore with size to let the #size threads connect to the resource at any time. 
import threading
from queue import Queue

class APIClient:
    def __init__(self):
        self._semaphore = threading.Semaphore(5)

    def make_request(self, endpoint: str):
        with self._semaphore:
            return self._http_client(endpoint)

    def _http_client(self, endpoint: str):
        pass

'''
lets say we have to pass some object into each thread when they connect to the end resource

Eg when we connect to the database, we not only have the limit on number of concurrent requests, 
we also want each thread to connect to the connection pool

we can use blocking queue to get the connection pool
'''

class DBConnect:
    def __init__(self, pool_size: int):
        self._connection_queue: Queue[str] = Queue(10)
        for _ in range(pool_size):  
            self._connection_queue.put(conn)

    def _connect(self) -> str:
        try:
            self._connection_queue.get(timeout=0.1) # to produce error 
        except self._connection_queue.Empty:
            raise RuntimeError(f"no connections available currently. get back in sometime.")

    def _disconnect(self, conn: str) -> None:
        self._connection_queue.put(conn)

    def execute_query(self, query: str):
        conn = self._connect()
        try:
            conn._execute(query)
        finally:
            self._disconnect(conn)
