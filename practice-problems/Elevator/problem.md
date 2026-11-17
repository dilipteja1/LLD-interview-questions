# Elevator

an elevator system manages multiple elevators serving different floors in building. 
once the person requests a elevator, the system should decide on which one to dispatch. 
passengers click the destination floor, the system needs to move elevators efficiently when handling multiple concurrent requests. 

## requirements

- how many elevators or floors we are dealing with. is this configurable

let say 3 elevators, with 10 floors. fixed for now. (possible extennsion)

- is it a simple up/down call for elevator or will we have a destinatoin panel where we select the destination and relevant elevator 
- gets assigned. 

no just simple buttonn. with up down calls. 

- a passenger can press multiple buttons inside a elevator. 

yes. they can press what ever they want. 

- should the hall calls be differed from the destination calls inside the lift. 

yes. hall calls is simple up and down. any lift can serve this request. but inside the lift, the destination should be reached by that particular lift only. 

- invalid requests. wrong floor numbers etc. 

if same floor dest is requested. it should be no op and should stop there. 

- should we worry about the capacity. door mechanics etc

lets keep it focused on scheduling and movement logic. 


## Entities

ElevatorController

- runs all the functionality required for orchestrating and sending the elevators up and down 

Elevator

- keeps track of one elevator. its current floor. destinations it should reach (pressed buttons) which is requests. available or not. 

Floor 

- keeps track of Elevators it currently has. floor number.

Request

- floor details. 

## Class Design

Elevator controller

lets the user start a request, assign the request to an elevator, let the elevator move one step at time to all the requested destinations

```python
class ElevatorController:
    - elevators: list[Elevator]
    - floors: list[Floor]
    - requests: list[Request]

    + requestElevator(Floor, request_type)
    + assignElevator(Request)
    + step() -> void
```

Elevator 

one single elevator. have the current floor details. any requests assigned to the elevator. The direction it is moving (it can only go in one direction and finish all requests in one direction first)

```python
class Elevator:
    - current_floor: Floor
    - assigned_requests: list[Requests]
    - current_direction: Direction

    + add_request(Request)
    + get_current_floor()
    + get_current_direction()
    + step() 
```

Request

it can be request from outside the elevator or a request from inside the elevator. it is a unified interface. 

```python
class Request:
    - floor: int
    - type: RequestType

    + get_type()
    + getFloor()

class RequestType:
    UP
    DOWN
    DESTINATION
```

## Extensions

- what if we want to have priority floors with express elevators

one elevator is dedicated to prioritize the floor. add a isExpress flag to one elevator and restrict their steps to only few floors. 

- what is we want to undo the request. 

we can implement a removeRequest method which removes the Request. if the elevator is in the transit. no-op

- concurrency
- what if the requestElevator call is givven concurently in the different floor. 


