import pygame
import random
from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()
prolog.consult("swish.pl")  # Load the Prolog file

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
PURPLE = (160, 32, 240) #HOME
YELLOW = (255, 223, 0)
BLUE = (135, 206, 250)
DARK_GREY = (169, 169, 169)

# Constants for grid elements
EMPTY = 0
PIT = -1
GOLD = 3
HOME = 2

# Initialize font
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)  # Use a font and size

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

player_font = pygame.font.SysFont("Arial", WIDTH)
 
# This sets the margin between each cell
MARGIN = 5
 
m = int(input("Enter your gridsize: "))
grid = []
for row in range(m):
    grid.append([])
    for column in range(m):
        grid[row].append(0)  # Append a cell
 
prolog.assertz(f"dim({m-1})")
# Starting position // 
x, y = random.randint(0, m - 1), random.randint(0, m - 1)
x1 = x
y1 = y
homex = x
homey = y
coins = 0
prolog.assertz(f"cell({x}, {y}, home)")

def get_adj(row, column, m):
  adj_coords = [(row+1, column), (row-1, column), (row, column+1), (row, column-1)]
  return [(x, y) for x, y in adj_coords if 0 <= x < m and 0 <= y < m]

def is_valid_pit_placement(x, y):
    if grid[x][y] != EMPTY:
        return False
    # Check neighbors for pits or home
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < m and grid[nx][ny] in {PIT, HOME}:
            return False
    return True

def is_valid_gold_placement(x, y):
    """Check if a gold coin can be placed at (x, y)."""
    if grid[x][y] != EMPTY:
        return False
    # Count adjacent gold coins
    adjacent_gold = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < m and grid[nx][ny] == GOLD:
            adjacent_gold += 1
    return adjacent_gold < 2
        
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [500, 500]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
 
# Set title of screen
pygame.display.set_caption("Adventure World")
 
# Loop until the user clicks the close button.
done = False
end = False
win = False
alive = True
grabbed = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Dynamic
grid[homex][homey] = 2
visited = set()
visited.add((homex, homey))
prolog.assertz(f"cell({homex}, {homey}, safe)")
list(prolog.query(f"safe({homex}, {homey})"))

# Place pits
pits_to_place = m - 2
while pits_to_place > 0:
    x, y = random.randint(0, m - 1), random.randint(0, m - 1)
    if is_valid_pit_placement(x, y):
        grid[x][y] = PIT
        prolog.assertz(f"cell({x}, {y}, pit)")
        for adj_x, adj_y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= adj_x < m and 0 <= adj_y < m and grid[adj_x][adj_y] == 0:
                prolog.assertz(f"cell({adj_x}, {adj_y}, breeze)")
        pits_to_place -= 1

# Place gold coins
gold_to_place = m - 1
while gold_to_place > 0:
    x, y = random.randint(0, m - 1), random.randint(0, m - 1)
    if is_valid_gold_placement(x, y):
        grid[x][y] = GOLD
        prolog.assertz(f"cell({x}, {y}, gold)")
        gold_to_place -= 1
'''
# For static
grid = [[0, 0, -1, 0, 0],
[0, 0, 0, 3, 3],
[0, 2, 0, 0, 0],
[3, 0, 0, 0, 0],
[-1, 0, 0, 3, -1]]

for row_index, row in enumerate(grid):
    for col_index, value in enumerate(row):
        if value == 2:
            homex = row_index
            homey = col_index
        elif value == 3:
            grid[row_index][col_index] = GOLD
            prolog.assertz(f"cell({row_index}, {col_index}, gold)")
        elif value == -1:
            grid[row_index][y] = PIT
            prolog.assertz(f"cell({row_index}, {col_index}, pit)")
            for adj_x, adj_y in [(row_index-1, col_index), (row_index+1, col_index), (row_index, col_index-1), (row_index, col_index+1)]:
                if 0 <= adj_x < m and 0 <= adj_y < m and grid[adj_x][adj_y] == 0:
                    prolog.assertz(f"cell({adj_x}, {adj_y}, breeze)")
            

print(homex, homey)
'''

x1 = homex
y1 = homey
coins = 0
m = len(grid)
grid[homex][homey] = 2
visited = set()
visited.add((homex, homey))
prolog.assertz(f"cell({homex}, {homey}, safe)")
list(prolog.query(f"safe({homex}, {homey})"))
#'''

for row in grid:
    print(row)
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        keys = pygame.key.get_pressed()
        if not end:
            if keys[pygame.K_LEFT] and y1 > 0:
                if grabbed:
                    prolog.assertz(f"cell({x1}, {y1}, grabbed)")
                    grabbed = False
                y1 -= 1
            if keys[pygame.K_RIGHT] and y1 < m - 1:
                if grabbed:
                    prolog.assertz(f"cell({x1}, {y1}, grabbed)")
                    grabbed = False
                y1 += 1
            if keys[pygame.K_UP] and x1 > 0:
                if grabbed:
                    prolog.assertz(f"cell({x1}, {y1}, grabbed)")
                    grabbed = False
                x1 -= 1
            if keys[pygame.K_DOWN] and x1 < m - 1:
                if grabbed:
                    prolog.assertz(f"cell({x1}, {y1}, grabbed)")
                    grabbed = False
                x1 += 1
                
            visited.add((x1, y1))
            list(prolog.query(f"addsafe({x1}, {y1})"))
            list(prolog.query(f"safe({x1}, {y1})"))
            
            #list(prolog.query(f"unknown({x1}, {y1})"))
            #list(prolog.query(f"setunsafe({x1}, {y1})"))
            
            adj = get_adj(x1, y1, m)
            for i in adj:
                visited.add(i)
            
            if grid[x1][y1] == 3: # Grab coin
                coins += 1
                grabbed = True
                
            if grid[x1][y1] == -1: # Dies to pit
                end = True 
                alive = False 
            
            if grid[x1][y1] == 2: # Home
                if keys[pygame.K_l] and coins > 1:
                    win = True
                    end = True 
                    
                if keys[pygame.K_l] and coins <= 1:
                    end = True
                
            grid[x1][y1] = 1
            grid[homex][homey] = 2
            
            # print("Grid coordinates: ", x1, y1)
            if keys[pygame.K_ESCAPE]:
                done = True
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(m):
        for column in range(m):
            color = GREY
            if row == x1 and column == y1:
                color = YELLOW
            elif grid[row][column] == 1:
                color = WHITE
            elif grid[row][column] == 2: #HOME
                color = PURPLE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            
            # Player position
            if row == x1 and column == y1:
                x_center = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y_center = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                text_surface = player_font.render("X", True, BLACK)
                text_rect = text_surface.get_rect(center=(x_center, y_center))
                screen.blit(text_surface, text_rect)
            
            # Inference Model Attempt
            # '''
            else:
                if (row,column) in visited:
                    xpos = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                    ypos = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                    
                    query_safe = list(prolog.query(f"cell({row}, {column}, safe)"))
                    
                    #list(prolog.query(f"unknown({row}, {column})"))
                    query_unsafe = list(prolog.query(f"cell({row}, {column},unsafe)"))
                    
                    temp = list(prolog.query(f"unsafe({row}, {column})"))
                    if temp:
                        list(prolog.query(f"addunsafe({row}, {column})"))
                    #query_unsafe = list(prolog.query(f"unsafe({row}, {column})"))
                    if query_safe:
                        list(prolog.query(f"addsafe({row}, {column})"))
                    elif query_unsafe:
                        list(prolog.query(f"addunsafe({row}, {column})"))
                    else:
                        list(prolog.query(f"addunknown({row}, {column})"))


                    if query_safe:
                        status = "S"
                    elif query_unsafe:
                        status = "U"
                    else:
                        status = "?"
                    #print ('Point(',row, column, ')' ,status)
                    # print ('Point(',adj_y, adj_x, ') Pos(', ypos, xpos,')' ,status)
                    text = font.render(status, True, BLACK)
                    text_rect = text.get_rect(center=(xpos, ypos), height=20, width=20)
                    screen.blit(text, text_rect)
                            # '''
                            
            if list(prolog.query(f"yesboth({x1}, {y1})")):
                text = f"Agent detects both a glitter and breeze. Player grabbed a coin."
                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 70))
            elif list(prolog.query(f"yesglitter({x1}, {y1})")):
                text = f"Agent detects a glitter. Player grabbed a coin."
                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 70))
            elif list(prolog.query(f"yesbreeze({x1}, {y1})")):
                text = f"Agent detects a breeze."
                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 70))
                
    if not end:      
        text = f"Player Coordinates: ({y1}, {x1})"
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 10))  # Position below the grid

        text = f"Coins Grabbed: {coins}"
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 30))
        if grid[x1][y1] == 2:
            text = f"Player is Home. Press L to leave."
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 50))
        else:
            text = f"Home is at ({homey}, {homex})."
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 50))
    else:
        if win:
            text = f"Mission accomplished! {coins} coin/s collected."
        else:
            if alive:
                text = f"Mission failed! Only {coins} coin/s collected."
            else:
                text = f"Mission failed! Player falls into a Pit."
            
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (MARGIN, (HEIGHT + MARGIN) * m + 10))  # Position below the grid

    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

print("Game Ended.")
pygame.quit()