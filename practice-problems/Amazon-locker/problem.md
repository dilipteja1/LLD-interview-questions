# Amazon locker

a locker system like amazon locker where delivery driver deposits packages and customers self-serve to pick them up using a code.

## Requirements

- how do we know which locker we should go

we pick the locker location while ordering. that will fix which locker we should be going 

- what are the sizes of the compartments

small to large. any sized package can go any locker which is equal or smaller that that. if there is no fit, reject the deposit. 

- what is in scope. 

once the package is in locker, thats where the scope starts. not the delivery routing etc. 

- what code the customer should get. email or sms

just return the code, the medium is someone else's problem

- what happens if the code is incorrect for multiple times

just return erro. do not go for lockout logic today

- Multi package pickup. should we have 1 token code or multiple

we should have 1 code per pickup delivery. No shared codes for pickups

- what is the TTL for the code. 

codes lets say expires after 7 days. if someone tries with expired code, then the staff should come nad help to retreive the code. 


## Entities and relationships

Compartment
AccessToken
Package - just to know the size to fit in the compartment
Locker - entry point for the orchestration of whole process. 

> state can be physical or relational. 
physical states are mentioned in the entities itself. 
relational states are mentioned in the orchestrator generally. 

## Class design

- needs a way to deposit package, get the code, let the user use the code, take the package, let staff open the compartment for expired tokens

```python
class Locker:
    - compartments
    - accessTokenMapping: Map<string, AccessToken>

    + Locker(compartments)
    + depositPackage(size) -> string  | error
    + pickup(tokencode) -> void | error
    + openExpiredCompartments() -> void
```

AccessToken 

- represents the bearer token for compartment access. should contain the code. should know if it expires

```python
class AccessToken: 
    - code: string
    - expiration: timestamp
    - compartment: Compartment

    # needs a way to check expired tokens

    + AccesToken(code, epiration, compartment)
    + isExpired() -> boolean
    + getCompartment() -> Compartment
    + getCode() -> String
```

Compartment

- easy. just the size of it and a boolean fro occupied or not

```python
class Compartment:
    - size: Size
    - occupied: boolean

    + getSize()
    + Compartment(size)
    + isOccupied() -> boolean
    + markOccupied() -> void
    + markFree() -> void
    + open() -> void
```

Size

```python
enum Size:
    SMALL
    MEDIUM
    LARGE
```

## extensions

- what if we want to place the package in the bigger compartment

check in the bigger sized compartments if they have an availabilty after checking in the current size slots

- what if any one of the compartment is under maintenance. 

we can track the health of the compartment in the compartment class. if it is out of service, we wont pick it. 

- what if the delivery guy does not deposit the package. we assumed that is not the case

then we should consider finding the compartment and depositing the package as two different operations. 
once we know that both the operations are done, then we can say that the deposit is success. 
reserve the compartment and do the deposit. 