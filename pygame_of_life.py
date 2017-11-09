from __future__ import print_function
import sys
from time import sleep
from random import randint, seed, choice
from argparse import ArgumentParser
import pygame

# Account for lack of xrange in py3
if sys.version_info[0] == 3:
    xrange = range


def gen_board(size, random=False):
    """Returns a blank or random board"""

    if random:
        return [[choice([False, False, False, True, True]) 
            for y in xrange(size)] for x in xrange(size)]  
    
    return [[False for y in xrange(size)] for x in xrange(size)]


def next_tick(cell_alive, number_of_neighbors): 
    """Returns a cell's state in the next turn
    
    Three conditions for the next state are layed out:
    1. A cell is alive and has 2/3 neighbors, it stays alive
    2. A cell is dead and has 3 neighbors, it is born
    3. Neither of the above, it dies
    """

    if cell_alive and number_of_neighbors in [2, 3]:
            return True
    elif not cell_alive and number_of_neighbors == 3:
            return True
    return False


def count_neighbors(x, y, board): 
    """Returns the number of neighbors a cell has"""
    size = len(board)
    return (                                 
        board[x               ][mod(y - 1, size)] +
        board[mod(x + 1, size)][mod(y - 1, size)] +
        board[mod(x + 1, size)][y               ] +
        board[mod(x + 1, size)][mod(y + 1, size)] +
        board[x               ][mod(y + 1, size)] +
        board[mod(x - 1, size)][mod(y + 1, size)] +
        board[mod(x - 1, size)][y               ] +
        board[mod(x - 1, size)][mod(y - 1, size)]   
    )


def mod(n, size): 
    """Returns the position of a cell based on modulo arithmetic"""
    size -= 1
    if n < 0:
        return size
    elif n > size:
        return 0
    return n


def main():
    """Main loop, defines game logic"""
    print("Controls: R - restart, Esc - quit")

    # Argument parser setup
    parser = ArgumentParser()
    parser.add_argument("-n", type = int, default = 64, 
                        help = "Number of cells", metavar = "")
    parser.add_argument("-s", type = int, default = 5, 
                        help = "Size of cells", metavar = "")
    parser.add_argument("-d", action = "store_true", 
                        help = "Enable debug mode")
    parser.add_argument("-t", type = float, default = 0.00, 
                        help = "Sets delay between ticks", 
                        metavar = "")
    parser.add_argument("-c", action = "store_true", 
                        help = "Enables colours")
    parser.add_argument("-k", type = int, default = 0, 
                        help = "Maximum life", metavar = "")
    parser.add_argument("-r", type = int, default = 0, 
                        help = "Max runtime of the game", metavar = "")

    # Variable setup
    args = parser.parse_args()
    cell_num = args.n
    cell_size = args.s
    debug_mode = args.d
    time_delay = args.t
    colour_enabled = args.c
    age_cap = args.k
    step_cap = args.r

    board = gen_board(cell_num, random=True)
    neighbors = gen_board(cell_num, random=False)
    cell_age = gen_board(cell_num, random=False)
    step_counter = 0

    # Pygame setup
    pygame.init()
    # Calculate and set displays size by generating a 2-tuple
    display = pygame.display.set_mode(
        (((cell_size + 1) * cell_num) - 1,) * 2)
    pygame.display.set_caption("Conway's Game of Life")

    # Colours
    c_black = (0, 0, 0)
    c_white = (255, 255, 255)
    c_red = (255, 0, 0)
    c_green = (0, 255, 0)
    c_blue = (0, 0, 255)

    while 1:
        # Get keypresses
        pygame.event.pump()
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_r] or (step_cap and step_counter > step_cap):
            board = gen_board(cell_num, random=True)
            step_counter = 0
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

        # Clear display
        display.fill(c_black)

        # Draw live cells
        for y in xrange(cell_num):
            for x in xrange(cell_num):
                if board[x][y]:
                    # Generate the square to be drawn
                    cell = pygame.Rect((cell_size + 1) * x, 
                                (cell_size + 1) * y, cell_size, cell_size)

                    # Draw the cell
                    if colour_enabled:
                        if cell_age[x][y] == 0:
                            pygame.draw.rect(display, c_blue, cell)
                        elif cell_age[x][y] in [1, 2, 3, 4, 5]:
                            pygame.draw.rect(display, c_white, cell)
                        elif cell_age[x][y] in [6, 7, 8, 9, 10, 11]:
                            pygame.draw.rect(display, c_red, cell)
                        else:
                            pygame.draw.rect(display, c_green, cell)
                    else:
                        pygame.draw.rect(display, c_white, cell)

                    cell_age[x][y] += 1
                else:
                    cell_age[x][y] = 0         

        pygame.display.update()
 
        # Count Neighbors
        for y in xrange(cell_num):
            for x in xrange(cell_num):
                neighbors[x][y] = count_neighbors(x, y, board)

        # Update board
        for y in xrange(cell_num):
            for x in xrange(cell_num):
                board[x][y] = next_tick(board[x][y], neighbors[x][y])

                if age_cap and cell_age[x][y] > age_cap:
                    board[x][y] = False

        step_counter += 1

        if not debug_mode:
            sleep(time_delay)
        else:
            sleep(0.500)

if __name__ == "__main__":
    main()
    sys.exit(0)
