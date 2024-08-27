import os
import time
import random
from os import name as osName
import perlin_noise

ALIVESTATE = 1
DEADSTATE = 0

def clean():
    if osName == "nt":
        os.system('cls')
    else:
        os.system('clear')


def display(tab):
    tabstr = ""
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            tabstr += tab[i][j]
        tabstr += "\n"
    print (tabstr)

# ----- RULES ----- #
def rule1(cell, adjacentCells):
    """Base game of life ruleset"""
    adjacent = 0
    for adjCell in adjacentCells:
        if adjCell in LIVING:
            adjacent += 1
    if cell in LIVING:
        if adjacent < 2:
            return DEADSTATE
        elif adjacent in [2,3]:
            return ALIVESTATE
        else:
            return DEADSTATE
    if cell in DEAD:
        if adjacent == 3:
            return ALIVESTATE
def rule2(cell, adjacentCells):
    """Idk, it makes cool pyramids"""
    adjacent = 0
    for adjCell in adjacentCells:
        if adjCell in LIVING:
            adjacent += 1
    # If cell is Alive
    if cell in LIVING:
        # If neighboors are superior or equal than 2 die
        if adjacent >= 1:
            return DEADSTATE
        # If top neighboor is alive, dies
        elif adjacentCells[0] in LIVING : return DEADSTATE

    # If Cell is dead:
    else :
        #if right or left neighboor is alive, comes to life
        if adjacentCells[2] in LIVING or adjacentCells[6] in LIVING:
            return ALIVESTATE
        # If all the bottom neighboors are alive, except the middle one, lives
        elif adjacentCells[3] in LIVING and adjacentCells[4] in DEAD and adjacentCells[5] in LIVING:
            return ALIVESTATE

def rule3(cell, adjacentCells):
    """single celled organisms"""
    adjacent = 0
    for adjCell in adjacentCells:
        if adjCell in LIVING:
            adjacent += 1
    #If alone, lives, else dies
    if cell in LIVING :
        if adjacent == 0: return ALIVESTATE
        else: return DEADSTATE

    elif cell in DEAD:
        #If the cell is neighboored by one diagonal cell, has 1/4 chance to become alive
        if adjacentCells[1] in LIVING or adjacentCells[3] in LIVING or adjacentCells[5] in LIVING or adjacentCells[7] in LIVING:
            if random.randint(1,4) == 4:
                return ALIVESTATE
        else: return DEADSTATE

def rule4(cell, adjacentCells):
    """Some rule i stole online"""
    adjacent = 0
    for adjCell in adjacentCells:
        if adjCell in LIVING:
            adjacent += 1
    # Death by overpopulation if neighbors > 7
    if adjacent > 7 : return DEADSTATE
    
    # Death by undepopulation if neighbors <2
    if adjacent < 2 : return DEADSTATE

    # Rebirth by reproduction if neighbors == 2
    if adjacent == 2 : return ALIVESTATE
def rule5(cell, adjacentCells):
    """Oh shit i created a blob"""
    adjacent = 0
    for adjCell in adjacentCells:
        if adjCell in LIVING:
            adjacent += 1
    if cell == ' ' and adjacent > 0 :
        return ALIVESTATE if random.randint(0,4) == 4 else DEADSTATE

def turn(grid,rule):
    #Copies ogTab to newTab to keep the initial background
    newgrid = []
    for i in range(height):
        newgrid.append(ogTab[i].copy())
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]

            topP =           [ ( i - 1 ) % height  , j   ]
            bottomP =        [ ( i + 1 ) % height , j    ]
            rightP =         [ i , ( j + 1 ) % width     ]
            leftP =          [ i , ( j - 1 ) % width     ]
            topleftP =       [ topP[0] ,  leftP[1]         ]
            toprightP =      [ topP[0] , rightP[1]         ]
            bottomrightP =   [ bottomP[0], rightP[1]       ]
            bottomleftP =    [ bottomP[0], leftP[1]        ]

            # Adds cells to a list in clock-wise order (top - ... - topleft)

            adjacentCells = [
                grid[topP[0]][topP[1]], # Top 0
                grid[toprightP[0]][toprightP[1]], # Top right 1
                grid[rightP[0]][rightP[1]], # Right 2
                grid[bottomrightP[0]][bottomrightP[1]], # Bottom right 3
                grid[bottomP[0]][bottomP[1]], # Bottom 4
                grid[bottomleftP[0]][bottomleftP[1]], # Bottom left 5
                grid[leftP[0]][leftP[1]], # Left 6
                grid[topleftP[0]][topleftP[1]] # Top left 7
            ]  

            cellIs = rule(cell, adjacentCells)
            if cell in DEAD:
                if cellIs == ALIVESTATE:
                    cell = random.choice(LIVING)
                else :
                    cell = ogTab[i][j]
            else :
                if cellIs == DEADSTATE:
                    cell = ogTab[i][j]
                else:
                    cell = cell
                
            newgrid[i][j] = cell
    
    clean()
    display(newgrid)
    return newgrid

if __name__ in "__main__":

    noise = perlin_noise.PerlinNoise(octaves=15, seed=random.randint(0,100))

    width = 225
    height = 50

    EMPTY = ' '
    DEAD = ['░', '▒', '▓' ,EMPTY]
    # LIVING = ['▄','█','▀','■']
    LIVING = ['■']
    # LIVING = ['■']
    
    #Background space creation
    ogTab = [[EMPTY for j in range(width)] for i in range(height)]
    for i in range(len(ogTab)):
        for j in range(len(ogTab[i])):
            perlin = noise([(i+1)/height,(j+1)/width])
            if perlin > 0.38 :  ogTab[i][j] = DEAD[2]
            elif perlin > 0.3 :  ogTab[i][j] = DEAD[1]
            elif perlin > 0.1 :  ogTab[i][j] = DEAD[0]
            else :               ogTab[i][j] = EMPTY 
            # ogTab[i][j] = str(round(perlin, ndigits=3))
    # Copying space to actual grid
    grid = []
    for i in range(height):
        grid.append(ogTab[i].copy())
    
    # Setup for rule4
    grid[25][115] = random.choice(LIVING)
    grid[2][117] = random.choice(LIVING)
    grid[3][117] = random.choice(LIVING)

    # Populates randomly
    for i in range(height):
        for j in range(width):
            if random.randint(0,4) >= 2:
                grid[i][j] = LIVING[random.randint(0,len(LIVING)-1)] 
    while(True):
        grid = turn(grid, rule2)
        time.sleep(0.06)
