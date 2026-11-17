"""
Elevator operations
"""

from dataclasses import dataclass
from enum import Enum
from collections import deque
from typing import Optional

class ElevatorController:
    def __init__(self, elevator_count: int, floor_count: int):
        self.elevator_count = elevator_count
        self.floor_count = floor_count
        self.elevators: list[Elevator] = []
        self._init_elevators()

    def _init_elevators(self) -> None:
        'initialize all the elevators'
        for id in range(self.elevator_count):
            elevator: Elevator = Elevator(id)
            self.elevators.append(elevator)

    def request_elevator(self, floor: int, type: RequestType) -> bool:
        '''
            1. validate the floor number
            2. pick the best elevator to handle the request
            3. add the request to best elevator
        '''
        if not 0 <= floor <= self.floor_count:
            return False
        if type == RequestType.DESTINATION:
            return False

        request: Request = Request(floor=floor, request_type=type)
        best_elevator: Optional[Elevator] = self.pick_best_elevator(request)
        if best_elevator is None:
            return False

        return best_elevator.add_request(request=request)

    def pick_best_elevator(self, current_request: Request) -> Optional[Elevator]:
        '''
            1. check the request direction. 
            2. iterate through elevators to check if any elevator 
            has requests to pass through the requested floor. 
            3. if no elevator has the requests. 
        '''
        floor: int = current_request.floor
        direction: Direction = (Direction.UP if current_request.request_type == RequestType.UP
                                else Direction.DOWN)

        on_the_way = [e for e in self.elevators if self._is_on_the_way(e, floor, direction)]
        idle = [e for e in self.elevators if e.get_current_direction == Direction.IDLE]

        # priority on_the_way > idle > anyone
        for candidates in (on_the_way, idle, self.elevators):
            if candidates:
                # select the nearest of the candidates
                return self._nearest(candidates, floor)

    @staticmethod
    def _is_on_the_way(elevator: Elevator, requested_floor: int, direction: Direction) -> bool:
        "check if the any requests of elevators can pass through floor in the"
        "given direction."
        # if elevator is moving in opposite direction
        if elevator.get_current_direction != direction:
            return False
        current_floor = elevator.get_current_floor()

        not_passed: bool = False
        if direction == Direction.UP and current_floor <= requested_floor:
            not_passed = True
        if direction == Direction.DOWN and current_floor >= requested_floor:
            not_passed = True

        return not_passed and elevator.has_requests_at_or_beyond(requested_floor=requested_floor, direction= direction)

    @staticmethod
    def _nearest(elevators: list[Elevator], floor: int) -> Elevator:
        return min(elevators, key=lambda e: abs(e.current_floor - floor))

class Direction(Enum):
    'Models the current direction of an elevator'
    UP = "Up"
    DOWN = "Down"
    IDLE = "Idle"


class Elevator:
    def __init__(self, id:int):
        self.id: int = id
        self.current_floor: int = 0
        self.direction = Direction.IDLE
        self.requests: set[Request]= set()

    def add_request(self, request: Request):
        requested_floor: int = request.floor
        if not  0 <= requested_floor <= 9:
            return False
        if requested_floor == self.current_floor:
            return True
        if request in self.requests:
            return True
        self.requests.add(request)

        return True

    def get_current_floor(self):
        'get the current floor of the elevator'
        return self.current_floor

    def get_current_direction(self):
        'get the current direction of the elevator'
        return self.direction

    def has_requests_at_or_beyond(self, requested_floor: int, direction: Direction):
        "check if we have a request which can go past floor. this lets the elevator"
        "take up the request"
        for request in self.requests:
            # request to go up
            if request.floor >= requested_floor and direction == Direction.UP:
                return True
            # request to go down
            if request.floor <= requested_floor and direction == Direction.DOWN:
                return True
        return False

    def step(self):
        "continue to go in one direction until all the requests in "
        "that direction as done. then reverse the direction"
        if not self.requests:
            self.direction = Direction.IDLE
            return

        # start the initial direction
        if self.direction == Direction.IDLE:
            self.direction = self._initial_direction()

        # stop the elevator at this step to serve passengers at this floor.
        if self._serve_current_floor():
            # if no requests left after serving the current floor
            if not self.requests:
                self.direction = Direction.IDLE

        # nothing left in this direction. turn around
        if not self.has_requests_ahead(self.direction):
            "reverse the direcion"
            self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP
            return

        # otherwise move one floor
        self.current_floor += 1 if self.direction == Direction.UP else -1

    def has_requests_ahead(self, direction: Direction):
        "return any requests in the given direction"
        if direction == Direction.UP:
            return any(req.floor > self.current_floor for req in self.requests)
        return any(req.floor < self.current_floor for req in self.requests)

    def _serve_current_floor(self):
        "check if there are any requests in this floor. hall calls or destination"
        request_type : RequestType = RequestType.UP if self.get_current_direction() == Direction.UP else RequestType.DOWN

        requests_for_current_floor: set[Request]= {Request(floor=self.current_floor, request_type=request_type), Request(floor=self.current_floor, request_type=RequestType.DESTINATION)}
        served = requests_for_current_floor & self.requests
        self.requests -= served
        return bool(served)

    def _initial_direction(self):
        "set the initial direction to which ever is closer. get the lower one for a tie."
        nearest: Request = min(self.requests, key = lambda req: (abs(req.floor - self.get_current_floor()), req.floor))
        return Direction.UP if nearest.floor > self.current_floor else Direction.DOWN


@dataclass(frozen=True, kw_only=True)
class Request:
    floor: int
    request_type: RequestType

# class Request:
#     "base class for a request"
#     def __init__(self, floor: int, request_type: RequestType):
#         self.floor = floor
#         self.request_type = request_type

#     def get_request_type(self) -> RequestType:
#         return self.request_type

#     def get_floor(self):
#         return self.floor

class RequestType(Enum):
    'Models the request outside or inside the elevator'
    UP = 1
    DOWN = 2
    DESTINATION = 3


