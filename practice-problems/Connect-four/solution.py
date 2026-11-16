"""
Consider impl happy path. 
then think of what can go wrong. invalid states, invalid inputs, boundary conditions. 

when writing the code, avoid premature optimization to avoid confusion. 
"""


from enum import Enum
from typing import Optional

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board: Board = Board()
        self.player1: Player = player1
        self.player2: Player = player2
        self.current_player: Player = player1
        self.state = GameState.INPROGRESS
        self.winner: Optional[Player] = None

    def makeMove(self, player: Player, col: int) -> bool:
        if self.state is not GameState.INPROGRESS:
            return False
        if player is not self.current_player:
            return False

        row: int = self.board.place_disc(col, player.get_color())
        if row == -1:
            return False
        
        if self.board.check_win(row, col, player.get_color()):
            self.state = GameState.WIN
            self.winner = player
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            if self.current_player == self.player2:
                self.current_player = self.player1
            elif self.current_player == self.player1:
                self.current_player = self.player2

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner

    def get_board(self) -> Board:
        return self.board

    def get_game_state(self):
        return self.state

class Board:
    def __init__(self, rows: int  = 6, cols: int = 7):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list[Optional[Color]]] = [[None] * self.cols for _ in range(self.rows)]

    def get_board_size(self) -> tuple[int, int]:
        return (self.rows, self.cols)

    def get_board(self) -> list[list[Optional[Color]]]:
        return self.grid

    def can_place(self, col: int) -> bool:
        if col < 0 or col >= self.cols:
            return False
        return self.grid[0][col] is None

    def place_disc(self, col: int, color: Color) -> int:
        if not self.can_place(col):
            return -1
        for row in range(self.rows-1, -1, -1):
            if self.grid[row][col] is None:
                self.grid[row][col] = color
                return row

        return -1

    def check_win(self, row: int, col: int, color: Color):
        # check boundaries
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        # check the color again
        if self.grid[row][col] != color:
            return False

        directions = [(0,1), (1,0), (1,1), (-1,1)]

        for dr, dc in directions:
            count = 1 # current disc placement

            # walk forward
            r, c = row + dr, col + dc
            while self._check_bounds(r, c) and self.grid[r][c] == color:
                count += 1
                r += dr
                c += dc

            # walk backward
            r, c = row - dr , col - dc
            while self._check_bounds(r, c) and self.grid[r][c] == color:
                count += 1
                r -= dr
                c -= dc

            if count >= 4:
                return True

        return False
            
    def _check_bounds(self, row: int, col: int) -> bool: 
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_full(self) -> bool:
        for col in range(self.cols):
            for row in range(self.rows):
                if self.grid[row][col] is None:
                    return False

        return True


class Player:
    def __init__(self, name: str, color: Color):
        self.name: str = name
        self.color: Color = color

    def get_name(self) -> str:
        return self.name

    def get_color(self) -> Color:
        return self.color

class GameState(Enum):
    INPROGRESS = 'INP'
    WIN = 'WIN'
    DRAW = 'DRAW'


class Color(Enum):
    RED = 'R'
    YELLOW = 'Y'



    
