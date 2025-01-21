import random
import time

from boat import Boat

# Constant
GRID_SIZE: int = 10
SEA: int = 0
LETTERS: list[str] = [chr(letter_code) for letter_code in range(ord('A'), ord('A') + GRID_SIZE)]

# Datas
aircraft_carrier: Boat = Boat([], 0, 5, False)
cruiser: Boat = Boat([], 0, 4, False)
destroyer: Boat = Boat([], 0, 3, False)
submarine: Boat = Boat([], 0, 3, False)
torpedo: Boat = Boat([], 0, 2, False)
fleet: list[Boat] = [aircraft_carrier, cruiser, destroyer, submarine, torpedo]
header: dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}


def board() -> list[list[int]]:
    """
    Define the grid before placing boats
    :return: grid
    """
    grid = []

    for _ in range(GRID_SIZE):
        y = []
        for _ in range(GRID_SIZE):
            y.append(SEA)
        grid.append(y)
    return grid


def init_board() -> list[list[int]]:
    """
    Initialize the grid with the boats
    :return: grid
    """
    grid = board()

    for boat in fleet:
        boat.direction = init_boat_direction()
        place_boats(boat, grid)
    return grid


def init_boat_direction() -> int:
    """
    Initialize the direction of boat
    :return: 0 for horizontal and 1 for vertical
    """
    return random.randint(0, 1)


def enough_space(tall: int, grid, x: int, y: int) -> bool:
    have_space = True

    for i in range(tall):
        if grid[x][y + i] != 0 and grid[x + i][y] != 0:
            have_space = False

    return have_space


def horizontal_coordinate(tall: int) -> tuple[int, int]:
    """
    Method for determinate line and column
    :param tall: boat tall
    :return: random x and y
    """
    return random.randint(0, (10 - tall)), random.randint(0, 9)


def vertical_direction(tall: int) -> tuple[int, int]:
    """
    Method for determinate line and column
    :param tall: boat tall
    :return: random x and y
    """
    return random.randint(0, 9), random.randint(0, (10 - tall))


def placing_boat(direction: int, tall: int, grid, x: int, y: int, boat: Boat) -> None:
    if direction == 0:
        for i in range(tall):
            grid[x + i][y] = tall
            boat.position.append((x + i, y))
    else:
        for i in range(tall):
            grid[x][y + i] = tall
            boat.position.append((x, y + i))


def place_boats(boat: Boat, grid) -> None:
    """
    Place boats randomly in the grid
    :param boat: each boat in the fleet
    :param grid: grid created
    """
    boat_tall: int = boat.tall
    well_placed: bool = False
    direction: int = boat.direction

    while not well_placed:
        if direction == 0:
            x = horizontal_coordinate(boat_tall)[0]
            y = horizontal_coordinate(boat_tall)[1]
            enough_space(boat_tall, grid, x, y)
        else:
            x = vertical_direction(boat_tall)[0]
            y = vertical_direction(boat_tall)[1]
            enough_space(boat_tall, grid, x, y)

        if enough_space(boat_tall, grid, x, y):
            placing_boat(direction, boat_tall, grid, x, y, boat)
            well_placed = True


def valid_coordinate(choice: str) -> bool:
    if choice[0].upper() in header.keys() and 0 <= int(choice[1:]) <= 10:
        return True
    return False


def shoot(guess: str, grid, player_grid) -> None:
    """
    Allow the user to choose a cell in the board
    :param guess: question to the user
    :param grid: board generate
    :param player_grid: board of the player
    """
    player_choice: str = input(guess)

    if valid_coordinate(player_choice):
        y: int = header.get(player_choice[0].upper())
        x: int = int(player_choice[1:]) - 1
        match grid[x][y]:
            case 1 | 2 | 3 | 4 | 5:
                print("\nTouché")
                grid[x][y] = "O"
                player_grid[x][y] = "O"
                if is_destroyed(x, y):
                    print("Le bateau est coulé!!")
            case 0:
                print("\nRaté")
                grid[x][y] = "X"
                player_grid[x][y] = "X"
            case "O" | "X":
                print("Vous avez déjà tiré à cette endroit!\n")
    else:
        print("Veuillez entrer des coordonnées valides!")


def is_destroyed(x: int, y: int) -> bool:
    for boat in fleet:
        if (x, y) in boat.position:
            boat.position.remove((x, y))
            if not boat.position:
                boat.sink = True
                return boat.sink
    return False


def all_destroyed_boats(grid) -> bool:
    """
    Method to indicate if all boats are destroyed
    :param grid: board with boats placed
    :return: true or false
    """
    boat_remaining = set()
    for row in grid:
        for cell in row:
            if isinstance(cell, int) and cell > 0:
                boat_remaining.add(cell)

    if not boat_remaining:
        print("Tous les bateaux ont été coulés !!")
        return True
    else:
        return False


def display_player_board(grid) -> None:
    """
    Display the player board
    :param grid: empty board
    """
    print("    ", end="")
    print("+---" * GRID_SIZE + "+", end="\n")
    print("    ", end="|")
    for x in range(GRID_SIZE):
        print(" {} |".format(LETTERS[x]), end="")
    print()
    print("+---" * (GRID_SIZE + 1) + "+")
    for index, row in enumerate(grid):
        row_number = index + 1
        row_str = " | ".join(str(cell) if isinstance(cell, str) else " " for cell in row)
        print(f"|{row_number:2} | {row_str} |")
        print("+---" * (GRID_SIZE + 1) + "+")


def play() -> None:
    """
    Method to launch the game until all boats are destroyed
    """
    party_grid = init_board()
    player_board = board()
    all_boat_destroyed = False

    while not all_boat_destroyed:
        display_player_board(player_board)
        shoot("Choisissez des coordonnées:\n", party_grid, player_board)
        all_boat_destroyed = all_destroyed_boats(party_grid)
        time.sleep(1)

    display_player_board(player_board)
    new_game = input("Voulez-vous rejouer? [Y/N] \n")
    if new_game.casefold() == "y":
        play()
    else:
        print("Au revoir et à bientôt!")


if __name__ == '__main__':
    play()
