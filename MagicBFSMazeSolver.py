'''Megan Perry
SWDV 610 Final Project
Spring 2022
Magic Maze Solver-BFS

This should save any maze that is formatted properly, but I included 2 mazes and start/end positions for
demo/testing purposes.  Uncomment/comment out the different mazes with their corresponding start/end coords to test.
'''

import graphics as g    #This graphics module was featured in a textbook https://mcsp.wartburg.edu/zelle/python/graphics.py
import coolQueue as q    #I created this class to have some of the simple queue methods that are needed
import time    #we will use this to slow the maze solving down so we can see the algorithm at work
import sys    #only needed this to be able to close window by clicking the x


#Set up the window:
win = g.GraphWin("Magic BFS Maze Solver", 500, 500)

rows = 10
columns = 10
num_of_maze_blocks = (rows * columns)
win.setCoords(0, 0, columns, rows)    #convert window to work with coordinate system instead of pixel counts for ease of design
win.setBackground("white")

#set up your maze
#use tuples for (x, y)coordinates
maze_coord_grid = [    #coords for all blocks of the whole maze inc walls, start, end-scaffolding to build maze on
        (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),
        (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),
        (3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),
        (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),
        (5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),
        (6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),
        (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),
        (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10),
        (9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),
        (10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10)
        ]

#can comment/uncomment wall_block coords with their start/end coords to test.  The walls are really what makes it a maze
'''
wall_block_coords = [    #using coordinates makes it easier to code the search algorithm, convert to rectangles for graphics later
        (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),
        (2,1),(2,4),(2,6),(3,1),(3,3),(3,4),(3,8),(3,10),
        (4,1),(4,6),(4,7),(4,8),(4,10),(5,1),(5,2),(5,4),(5,10),
        (6,1),(6,2),(6,4),(6,6),(6,8),(6,10),(7,1),(7,4),(7,5),(7,6),(7,8),(7,10),
        (8,1),(8,3),(8,4),(8,6),(8,10),(9,1),(9,8),(9,10),
        (10,1),(10,2),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10)
        ]
start_block_coords = (2, 10)    #start and end coords also need to be taken out of the walls if you are creating your own maze
end_block_coords = (10, 3)

'''

#can comment/uncomment wall_block coords with their start/end coords to test.  The walls are really what makes it a maze
wall_block_coords = [    #using coordinates makes it easier to code the search algorithm, convert to rectangles for graphics later
        (1,1),(1,2),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),
        (2,1),(2,10),(3,1),(3,3),(3,4),(3,6),(3,7), (3,8), (3,10),
        (4,1),(4,6),(4,8),(4,10),(5,1),(5,2),(5,4),(5,5),(5,6),(5,10),
        (6,1),(6,5),(6,8),(6,10),(7,1),(7,3),(7,5),(7,7),(7,8),(7,10),
        (8,1),(8,2),(8,3),(8,5),(8,7),(8,10),(9,1),(9,7),(9,8),(9,10),
        (10,1),(10,2),(10,3),(10,4),(10,5),(10,7),(10,8),(10,9),(10,10)
        ]
start_block_coords = (1,3)
end_block_coords = (10, 6)
       

#convert and draw maze and components-Graphics work-

def make_maze_walls(wall_block_coords):    #make list of rectangles that are wall blocks
    rect_wall_blocks = []
    for each in wall_block_coords:    #convert coordinates to rectangles for graphics
        x = each[0]
        y = each[1]
        wall_rect = g.Rectangle(g.Point((x-1), (y-1)), g.Point(x, y))
        rect_wall_blocks.append(wall_rect)
    return rect_wall_blocks

def draw_maze_walls(rect_wall_blocks):    #draw the maze walls
    for each in rect_wall_blocks:
        each.setFill("black")
        each.draw(win)

def draw_start_block(start_block_coords):    #make start easy to see for user
    x = start_block_coords[0]
    y = start_block_coords[1]
    rect_start = g.Rectangle(g.Point((x-1), (y-1)), g.Point(x, y))    #convert coords to rectangles for graphics
    rect_start.setFill("green")
    rect_start.draw(win)

def draw_end_block(end_block_coords):    #make end goal easy to see
    x = end_block_coords[0]
    y = end_block_coords[1]
    rect_start = g.Rectangle(g.Point((x-1), (y-1)), g.Point(x, y))    #convert coords to rectangles for graphics
    rect_start.setFill("blue")
    rect_start.draw(win)
    
def draw_path_list(path_list, color):  #show the user the search algorithm in action visually
    rect_path_list = []
    for each in path_list:    #convert coordinates to rectangles for graphics
        x = each[0]
        y = each[1]
        rect_path_block = g.Rectangle(g.Point((x-1), (y-1)), g.Point(x, y))
        rect_path_list.append(rect_path_block)
        
    for each in rect_path_list:
        each.setFill(color)
        each.draw(win)
    
#This is the guts of the program-where the magic happens-functions that make BFS work-finding each adjacent item and processing them
        
def bfs_solve_maze(start_block_coords, end_block_coords, wall_block_coords, rows, columns):    #pass in maze components-coordinates
    path_queue = q.CoolQueue()    #make a queue to hold current blocks and path
    #add tuples to queue-initialize with (start coords-currentblock, [startcoords-will be a path list]
    path_queue.push((start_block_coords, [start_block_coords]))
    discovered_neighbors = []    #list of neighbor coords we already looked at-will check later so we don't backtrack/repeat moves
    
    #loop to examine neighbors (will call on other functions within), throw out bad ones and add good/valid ones to path
    while path_queue.is_empty() == False:    #while the queue still has neighbors in it to evaluate
        #pop queue, get current coords (to evaluate) and the path to track
        current_coords, path_list = path_queue.pop()
        x, y = current_coords
        
        draw_path_list(path_list, "gray")    #graphics to draw the paths as they are growing
        time.sleep(0.1)
        
        if current_coords == end_block_coords:  #If you made it to the end, you "won"-stop the search!
            solution = draw_path_list(path_list, "magenta")    #graphics to show the winning path-it made it to the end first
            
            win.getMouse()    #jsut some options to close out of the program for user convenience
            win.close()

        #call upon these functions to find and screen the neghbors     
        potential_neighbors = get_neighbors(rows, columns, x, y)
        keep_good_neighbors(potential_neighbors, discovered_neighbors, path_list, path_queue)
        

#Find adjacent neighbors, will do this for each level/loop that we do
def get_neighbors(rows, columns, x, y):
    potential_neighbors = [] #store the neighbors!
    
    if x > 1:    #stay within the maze grid
        potential_neighbors.append(((x - 1), y)) #left neighbor
    if x < columns:
        potential_neighbors.append(((x + 1), y)) #right neighbor
    if y > 0:
        potential_neighbors.append((x, (y - 1))) #neighbor below
    if y < rows:
        potential_neighbors.append((x, (y +1)))  #neighbor above
    return potential_neighbors
#Only keep good neighbors to process-can't be a wall or one that we already used    
def keep_good_neighbors(potential_neighbors, discovered_neighbors, path_list, path_queue):
    for valid_neighbor in potential_neighbors:
        if valid_neighbor in discovered_neighbors:    #check if in discovered-don't need to repeat moves
            continue    #move on to next iteration if in discovered and don't move forward with that neighbor, check next one
     
        if valid_neighbor in wall_block_coords:    #check if in wall blocks, can't make a path on the wall barriers
            continue    #go to next iteration and don't do anything with these coords if they're a wall block
        
        valid_path = path_list + [valid_neighbor]    #add this verified valid neighbor to the path list
        path_queue.push((valid_neighbor, valid_path))    #put the valid neighbor in queue and keep track of path
        discovered_neighbors.append(valid_neighbor)    #add to discovered so we don't revisit/reprocess this one
    
    
#call functions to run the program:
w = make_maze_walls(wall_block_coords)
draw_maze_walls(w)
draw_start_block(start_block_coords)
draw_end_block(end_block_coords)
bfs_solve_maze(start_block_coords, end_block_coords, wall_block_coords, rows, columns)

sys.exit()
        

        


    

        


