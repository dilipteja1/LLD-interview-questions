# design of the locking mechanism to achieve the correctness

import threading
from typing import Dict, Optional
'''
Coarse grained locking

lock the entire data structure to update it serially
'''
class TicketBooking:
    def __init__(self):
        self.lock = threading.Lock()
        self.seat_owners: Dict[str, str] = {}

    def book_seat(self, seat_id: str, visitor_id: str) -> bool:
        # do not release the lock until we check and update. 
        with self.lock:
            if seat_id in self.seat_owners:
                return False
            self.seat_owners[seat_id] = visitor_id
            return True

'''
read write locks

case where there can be so many reads but only few writes here and there. 
sometimes called shared exclusive lock. 
'''
class Cache:
    def __init__(self):
        self._lock = threading.RLock() # reentrant lock allows permit the lock to the same thread any # of times
        self._read_count = 0
        self._read_count_lock = threading.Lock()

        self._data: Dict[str, str] = {}

    def get(self, key: str):
        with self._read_count_lock:
            self._read_count += 1
            if self._read_count == 1:
                self._lock.acquire()
        try:
            value: Optional[str] = self._data.get(key, None)
            if value is None: 
                print(f"{key} is not present in the cache")
        finally:
            with self._read_count_lock:
                self._read_count -= 1
                if self._read_count == 0:
                    self._lock.release()
        return value


    def put(self, key:str, value: str) -> bool:
        with self._lock:
            self._data[key] = value
            return True

        return False
            
'''
fine grained locks. lock each seat in the theater instead of all the seats
'''
class TicketBooking:
    def __init__(self):
        self._seat_locks_lock: threading.Lock = threading.Lock()
        self._seat_locks: Dict[str, threading.Lock] = {}
        self.seats: Dict[str, str] = {}

    def _get_lock(self, seat_id: str):
        with self._seat_locks_lock:
            if seat_id not in self._seat_locks:
                self._seat_locks[seat_id] = threading.Lock()
            return self._seat_locks[seat_id]

    def book(self, seat_id: str, visitor_id: str) -> bool:
        with self._seat_locks[seat_id]:
            if seat_id in self.seats:
                return False
            if seat_id not in self.seats:
                self.seats[seat_id] = visitor_id
            return True
        return False

## challenge is when two users want to swap the seats. they try to lock each other seats and try to get the other seat which will be deadlock. 
## we can fix this by locking only the chronologically small seat. 

