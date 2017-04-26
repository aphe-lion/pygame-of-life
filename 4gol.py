import pygame
from time import sleep
from random import randint, seed, choice
from argparse import ArgumentParser

# Board initialising
def gen_blank_board(size):
    # Return 2d list of 0s using list comprehension
    return [[0 for y in xrange(size)] for x in xrange(size)]

# Board initialising
def gen_random_board(size):
    # Return 2d list of random 1s and 0s using list comprehension
    return [[choice([0, 0, 0, 1, 1]) for y in xrange(size)] \
            for x in xrange(size)]

# Determines cell state in a new tick
def next_tick(cell, neighbors): 
    if cell and neighbors in [2, 3]:
            return 1
    elif not cell and neighbors == 3:
            return 1
    return 0

# Counts a cell's neighbors
def count_neighbors(x, y, board, size): 
    # Return the summed value of the neighboring cells
    return int(                                 
        board[x             ][mod(y - 1, size)] +  
        board[mod(x + 1, size)][mod(y - 1, size)] +  
        board[mod(x + 1, size)][y             ] +  
        board[mod(x + 1, size)][mod(y + 1, size)] +  
        board[x             ][mod(y + 1, size)] +  
        board[mod(x - 1, size)][mod(y + 1, size)] +  
        board[mod(x - 1, size)][y             ] +  
        board[mod(x - 1, size)][mod(y - 1, size)]   
    )

# Psuedo-modulo function, used to make a torus
def mod(n, size): 
    size -= 1
    if n < 0:
        return size
    elif n > size:
        return 0
    return n

# This is were the magic happens
def main():
    # Print controls
    print "Controls: R - restart, Esc - quit"

    # Argsparse setup
    parser = ArgumentParser()
    parser.add_argument("-n", type = int, default = 64, 
                        help = "Number of cells", metavar = "")
    parser.add_argument("-s", type = int, default = 5, 
                        help = "Size of cells", metavar = "")
    parser.add_argument("-d", action = "store_true", 
                        help = "Enable debug mode")
    parser.add_argument("-t", type = float, default = 0.03, 
                        help = "Sets delay between ticks", 
                        metavar = "")
    parser.add_argument("-c", action = "store_true", 
                        help = "Enables colours")
    parser.add_argument("-k", type = int, default = 0, 
                        help = "Maximum life", metavar = "")

    # Variable setup
    args = parser.parse_args()
    cell_num = args.n
    cell_size = args.s
    debug_mode = args.d
    time_delay = args.t
    colour_enabled = args.c
    age_cap = args.k

    board = gen_random_board(cell_num)
    neighbors = gen_blank_board(cell_num)
    cell_age = gen_blank_board(cell_num)

    # Pygame setup
    pygame.init()
    displaySize = ((cell_size + 1) * cell_num) - 1
    displaySize = (displaySize, displaySize)
    display = pygame.display.set_mode(displaySize)

    pygame.display.set_caption("Conway's Game of Life")
    c_black = (0, 0, 0)
    c_white = (255, 255, 255)
    c_red = (255, 0, 0)
    c_blue = (0, 255, 0)
    c_green = (0, 0, 255)

    # Main loop, do forever
    while 1: # True:
        # Get keypresses
        pygame.event.pump()
        keys_pressed = pygame.key.get_pressed()

        # Act on pressed keys
        if keys_pressed[pygame.K_r]:
            board = gen_random_board(cell_num) 
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

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
                        elif cell_age[x][y] in [1, 2, 3, 4, 5, 6]:
                            pygame.draw.rect(display, c_white, cell)
                        else:
                            pygame.draw.rect(display, c_green, cell)
                    else:
                        pygame.draw.rect(display, c_white, cell)
                    # Increase cell age
                    cell_age[x][y] += 1
                else:
                    cell_age[x][y] = 0         

        # Update display
        pygame.display.update()
 
        # Count Neighbors
        for y in xrange(cell_num):
            for x in xrange(cell_num):
                neighbors[x][y] = count_neighbors(x, y, board, cell_num)

        # Update board
        for y in xrange(cell_num):
            for x in xrange(cell_num):
                board[x][y] = next_tick(board[x][y], neighbors[x][y])
                if age_cap and cell_age[x][y] > age_cap:
                    board[x][y] = 0

        # Delay if in debug mode
        if not debug_mode:
            sleep(time_delay)
        else:
            sleep(0.100)

if __name__ == "__main__":
    main()
