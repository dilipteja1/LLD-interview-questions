"""
 design the happy path

 Amazon Locker
"""

from typing import Optional, Dict
from datetime import datetime, timedelta
from enum import Enum
import random

class Locker:
    def __init__(self, compartments: list[Compartment]):
        self.compartments: list[Compartment] = compartments
        self.access_token_mapping: Dict[str, AccessToken] = {}

    def depositPackage(self, size: Size) -> str:
        """
            1. find the available compartment
            2. generate access token
            3. mark the compartment occupied. 
            4. store access token in the lookup map. 
        """
        available_compartment: Optional[Compartment] = self._get_available_compartment(size = size)
        if available_compartment is None:
            raise Exception(f"No available compartments for size {Size.value}")

        available_compartment.open()
        available_compartment.mark_occupied()
        access_token: AccessToken = self._generate_access_token(available_compartment)
        code: str = access_token.get_code()
        self.access_token_mapping[code] = access_token

        return code

    def _get_available_compartment(self, size: Size) -> Optional[Compartment]:
        "validate and get an available compartment if there is one"
        for compartment in self.compartments:
            if compartment.get_size() == size and not compartment.is_occupied():
                return compartment
        return None

    def _generate_access_token(self, compartment: Compartment):
        "generate random access token for the compartment"
        code: str = f"{random.randint(0,99999):06d}"
        expiration: datetime = datetime.now() + timedelta(days=7)
        access_token: AccessToken = AccessToken(code, compartment=compartment, expiration=expiration)

        return access_token

    def pickupPackage(self,code: str) -> None:
        "enter the code for package pickup"
        access_token: Optional[AccessToken] = self.access_token_mapping.get(code, None)
        if access_token is None:
            raise Exception("Access token is not present in the map. Please contact the personnal for next steps.")
        if access_token.is_expired():
            raise Exception("Access token is expired. Please contact the personnal for next steps.")

        compartment: Compartment = access_token.get_compartment()
        compartment.open()
        compartment.mark_free()
        self.access_token_mapping.pop(code, None) # remove the code entry in the dict. 


class Compartment:
    def __init__(self, size: Size):
        self.size: Size = size
        self.occupied = False

    def get_size(self) -> Size:
        return self.size

    def is_occupied(self) -> bool:
        "check if the compartment is occupied"
        return self.occupied

    def mark_occupied(self) -> None:
        "Mark the compartment to occupied"
        self.occupied = True

    def mark_free(self) -> None:
        "Mark the compartment free"
        self.occupied = False

    def open(self) -> None:
        "out of scope logic. open the compartment."
        pass

class AccessToken:
    def __init__(self, code: str, expiration: datetime, compartment: Compartment):
        self.code = code
        self.expiration = expiration
        self.compartment = compartment

    def is_expired(self) -> bool:
        "check if the code is expired"
        return datetime.now() >= self.expiration

    def get_compartment(self) -> Compartment:
        "get the compartment corresponding to the access token"
        return self.compartment

    def get_code(self) -> str:
        "get the code for the accesstoken"
        return self.code

class Size(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"