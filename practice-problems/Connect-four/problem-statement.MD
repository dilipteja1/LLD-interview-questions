# Connect-four

two player game. they take turns to place their pieces in 7*6 grid. the first player to put 4 of their pieces
in a row, column or diagonal wins. 

## Requirements

- Goal is to get the concrete spec early

Q1 - can we select random row and column

No, we select the column and it takes the lowest available spot. think of gravity pulling the disc to the lowest possible place. 

Q2 - what is the end conditions for the game

Either row, column or diagonal is filled or if all the slots are filled without a winner, its a draw

Q3 - what are the boundaries. if someone tries to drop a disc in the full column

return false and raise an error. dont let invalid moves break the game. 

Q4 - do we have concurrent games played

No, just one game at a time

Q5 - do we have UI support planned just so that the design will have some print API's to help render

No, just the backend suppprt

Q6 - Do we track history or support undo. 

No, dont over complicate it 

Q7 - can board be configurable or fixed

Fixed, for now 7*6

## core entities

Game - have the logic for playing and ending of game
Player - logic related to the players
Board - logic related to the slots in the game

- define both state and behaviour for each entities

## class design

Game

- track whose turn is it
- track the current state of the board to conclude the game - game state
- who won. player 1 or player 2

> lets have a enum for game state to enforce the correctness

```python
class game:
    - board : Board()
    - player1 : Player()
    - player2 : Player()
    - currentPlayer : Player()
    - state : GameState
    - winner : Player? # optional. NULL if no winner and draw

    + Game(player1, player2)
    + makeMove(player, column) -> bool
    + getCurrentPlayer() -> Player
    + getWinner() -> Player?
    + getBoard() -> Board() # for UI rendering purposes
```

Board

 - Tracks all the cols and rows of the board. 
 - contains two different colors across the board
 - keep colors to the grid rather than player info. this is purely for easy testability

 ```python
    class board:
        - rows: int
        - cols: int
        - grid: DiscColor?[rows][cols] # can be null if empty or just started. 

        + Board()
        + getRows()
        + getCols()
        + canPlace(Column) -> bool
        + placeDisc(column, color) -> int # returns the row when disc lands
        + isFull() -> bool
        + checkWin(row, column, color) -> bool # check all possibilities of winning
        + getCell(row, column) -> discColor? # can be empty due to no color. 
 ```

 Player

 - represents one participant of the game
 - disc color assigned to the player. 

 ```python
    - name : string
    - color : DiscColor

    + Player(name, color)
    + getName() -> string
    + getcolor() -> DiscColor
 ```

 DiscColor 

 - Enum for colors

 ```python
    enum DiscColor:
        RED
        YELLOW
```

GameState

- State machine for the game. used in the Game class

```python
    enum GameState:
        IN_PROGRESS
        WON
        DRAW
```

## Extensions

- What if the second player is a bot. 

when computer / bot plays the game, we need to make an automatic move for that.
create a Player interface and implement HumanPlayer and BotPlayer classes on top of them. That will be a cleaner approach. 
Also for bot, add a botEngine which comes up with a col to play. 

- How to add a undo functionality

for undo, we need to add a history stack. In Game class, we moveHistory when we have a new event. if we have to undo, we pop the event from the stack and hydrate the other classes with relevant state. 