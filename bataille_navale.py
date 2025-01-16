import random
import time

# Datas
aircraft_carrier = [5,5]
cruiser = [4,4]
destroyer = [3,3]
submarine = [2,3]
torpedo = [1,2]
fleet = [aircraft_carrier, cruiser, destroyer, submarine, torpedo]
header = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}

def board():
    """
    Define the grid before placing boats
    :return: grid
    """
    grid = []

    for i in range(10):
        y = []
        for j in range(10):
            y.append(0)
        grid.append(y)
    return grid

def init_board():
    """
    Initialize the grid with the boats
    :return: grid
    """
    grid = board()

    for boat in fleet:
        place_boats(boat, grid)
    return grid

def place_boats(boat, grid):
    """
    Place boats randomly in the grid
    :param boat: each boat in the fleet
    :param grid: grid created
    """
    boat_number = boat[0]
    boat_tall = boat[1]
    x_direction = 0
    well_placed = False
    direction = random.randint(0,1)

    while not well_placed:
        have_space = True
        if direction == x_direction:
            x = random.randint(0, (10 - boat_tall))
            y = random.randint(0, 9)
            for i in range(boat_tall):
                if grid[x + i][y] != 0:
                    have_space = False
        else:
            x = random.randint(0, 9)
            y = random.randint(0, (10 - boat_tall))
            for i in range(boat_tall):
                if grid[x][y + i] != 0:
                    have_space = False

        if have_space:
            if direction == x_direction:
                for i in range(boat_tall):
                    grid[x + i][y] = boat_number
            else:
                for i in range(boat_tall):
                    grid[x][y + i] = boat_number
            well_placed = True

def shoot(guess, grid, player_grid):
    """
    Allow the user to choose a cell in the board
    :param guess: question to the user
    :param grid: board generate
    :param player_grid: board of the player
    """
    player_choice = input(guess)

    y = header.get(player_choice[0].upper())
    x = int(player_choice[1:]) - 1
    match grid[x][y]:
        case 1 | 2 | 3 | 4 | 5:
            print("\nTouché")
            grid[x][y] = "O"
            player_grid[x][y] = "O"
        case 0:
            print("\nRaté")
            grid[x][y] = "X"
            player_grid[x][y] = "X"
        case "O" | "X":
            print("Vous avez déjà tiré à cette endroit!\n")

def destroyed_boat(grid):
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

    if  not boat_remaining:
        print("Tous les bateaux ont été coulés !!")
        return True
    else:
        return False

def display_player_board(grid):
    """
    Display the player board
    :param grid: empty board
    """
    print("    +---+---+---+---+---+---+---+---+---+---+")
    print("    | A | B | C | D | E | F | G | H | I | J |")
    print("+---+---+---+---+---+---+---+---+---+---+---+")
    for index,row in enumerate(grid):
        row_number = index + 1
        row_str = " | ".join(str(cell) if isinstance(cell, str) else " " for cell in row)
        print(f"|{row_number:2} | {row_str} |")
        print("+---+---+---+---+---+---+---+---+---+---+---+")

def play():
    """
    Method to launch the game until all boats are destroyed
    """
    party_grid = init_board()
    player_board = board()
    all_boat_destroyed = False

    while not all_boat_destroyed:
        display_player_board(player_board)
        shoot("Choisissez des coordeonnées:\n", party_grid, player_board)
        all_boat_destroyed = destroyed_boat(party_grid)
        time.sleep(1)
    else:
        display_player_board(player_board)
        new_game = input("Voulez-vous rejouer? [Y/N] \n")
        if new_game.casefold() == "y":
            play()
        else:
            print("Au revoir et à bientôt!")

if __name__ == '__main__':
    play()