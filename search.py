from operator import truediv
from os import environ
from re import L
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import sys


class Grid:
    block_width=30
    width = 600
    height = 600
    gray = [41,41,41]
    line_color= [229,229,229]
    neighbors_list = {}

    def __init__(self):
        pygame.init()  #intializes pygame
        self.screen = pygame.display.set_mode((self.width, self.height)) #makes dimensions 600x600
        pygame.display.set_caption("Maze") #name is maze
        self.screen.fill(self.gray) #sets background to gray
        pygame.display.flip() #displays the screen


    def setup_blocks(self):
        accumulator=0 #accumulator for neighbors. These will be the indices of the grid
        y=0 #needed this so that column starts at 20
        y_index=-1 #need this so that y coord index starts at 0 in for loop
        for i in range(20): #20 iterations because width divided by block_width
            y_index=y_index+1 #iterate y coordinate
            x=self.block_width  
            y=y +self.block_width  #iterating each column
            for j in range(20):
                self.neighbors(accumulator)
                accumulator=accumulator+1
                pygame.display.flip()
                pygame.draw.line(self.screen , self.line_color, (x, y), (x, y+30)) #draws line down of current coord
                pygame.draw.line(self.screen , self.line_color, (x, y), (x+30, y))#draws line right of current coord
                pygame.draw.line(self.screen , self.line_color, (x, y), (x, y-30))#draws line up of current coord
                pygame.draw.line(self.screen , self.line_color, (x, y), (x-30, y))#draws line left of current coord
                pygame.display.flip() #updating display
                x=self.block_width+x #iterating each row
        
     
    def highlight_box(self, position):
        if position[0] ==0 and position[1]==0: #this is used so that the board doesn't highlight first
            #indice at initialization
            return
        color = [240,248,255] #highlight color around whitish
        x_indice = position[0]//30 #to find the left coords of current position of current block your in
        y_indice = position[1]//30 #to find the top coords of current position of current block your in
        pygame.draw.rect(self.screen, color, pygame.Rect(x_indice*30, y_indice*30, 30, 30)) # draw rectangle of current block
        #this is the highlight for the user
        pygame.display.flip() #this displays the highlighted block
        #this redraws the highlighted block to original block with white lines. We don't display it
        pygame.draw.rect(self.screen, self.gray, pygame.Rect(x_indice*30, y_indice*30, 30, 30)) 
        pygame.draw.line(self.screen , self.line_color, (x_indice*30, y_indice*30), (x_indice*30+ 30, y_indice*30) )
        pygame.draw.line(self.screen , self.line_color, (x_indice*30, y_indice*30), (x_indice*30 , y_indice*30+30) )
        pygame.draw.line(self.screen , self.line_color, (x_indice*30 +30, y_indice*30+30), (x_indice*30+30, y_indice*30-30))
        pygame.draw.line(self.screen , self.line_color, (x_indice*30 +30, y_indice*30+30), (x_indice*30 - 30 , y_indice*30+30))

    def neighbors(self, acc):
        neigh_list=[]
        if acc % 20 == 0 and acc/20<1: #if indice is top_left
            neigh_list.append(acc+1) #neighbor is right indice
            neigh_list.append(acc+20) #neighbor is bottom indice
            self.neighbors_list[acc] = neigh_list
        elif acc % 20 == 0 and acc/380>=1: #if indice is bottom_left
            neigh_list.append(acc+1) #neighbor is right indice
            neigh_list.append(acc-20) #neight is top indice
            self.neighbors_list[acc] = neigh_list
        elif acc % 20 == 19 and acc/20<1: #if indice is top_right
            neigh_list.append(acc-1) #neighbor is left indice
            neigh_list.append(acc+20) #neighbor is bottom indice
            self.neighbors_list[acc] = neigh_list
        elif acc % 20 == 19 and acc/380>=1: #if indice is bottom_right
            neigh_list.append(acc-1) #neighbor is left indice
            neigh_list.append(acc-20) #neighbor is top indice
            self.neighbors_list[acc] = neigh_list
        elif acc % 20 == 19: #if indice is right edge
            neigh_list.append(acc-1)
            neigh_list.append(acc-20)
            neigh_list.append(acc+20)
            self.neighbors_list[acc] = neigh_list
        elif acc/380>=1: #if indice is bottom edge
            neigh_list.append(acc-1)
            neigh_list.append(acc-20)
            neigh_list.append(acc+1)
            self.neighbors_list[acc] = neigh_list
        elif acc/20<1: #if indice is top edge
            neigh_list.append(acc-1)
            neigh_list.append(acc+20)
            neigh_list.append(acc+1)
            self.neighbors_list[acc] = neigh_list
        elif acc % 20 == 0: #if indice is left edge
            neigh_list.append(acc+1)
            neigh_list.append(acc+20)
            neigh_list.append(acc-20)
            self.neighbors_list[acc] = neigh_list
        else: #no edge or corner case, just in the middle
            neigh_list.append(acc+1)
            neigh_list.append(acc-1)
            neigh_list.append(acc+20)
            neigh_list.append(acc-20)
            self.neighbors_list[acc] = neigh_list

    def build_wall(self, pos):
        color = [139,119,101] 
        x_indice = pos[0]//30 #to find the left coords of current position of current block your in
        y_indice = pos[1]//30 #to find the top coords of current position of current block your in
        pygame.draw.rect(self.screen, color, pygame.Rect(x_indice*30, y_indice*30, 30, 30)) # draw rectangle of current block
        pygame.display.flip() #this displays the highlighted block
        indice = 20*y_indice + x_indice
        
        for i in self.neighbors_list[indice]:
            if indice in self.neighbors_list[i]:
                self.neighbors_list[i].remove(indice)
            
        return indice

    #breadth first search
    def bfs(self, graph, start, goal):
        # keep track of explored nodes
        explored = []
        # keep track of all the paths to be checked
        queue = [[start]]
 
        # return path if start is goal
        if start == goal:
            return "That was easy! Start = goal"
 
        # keeps looping until all possible paths have been checked
        while queue:
            # pop the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1]
            if node not in explored:
                neighbours = graph[node]
                # go through all neighbour nodes, construct a new path and
                # push it into the queue
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if neighbour == goal:
                        return new_path
 
                # mark node as explored
                explored.append(node)

    def draw_path(self, shortest_path):
        path = [187,255,255]
        
        for i in range(len(shortest_path)):
            y_indice = shortest_path[i]//20
            x_indice = shortest_path[i]-(20*y_indice)
            x_coord = x_indice*30
            y_coord= y_indice*30
            pygame.draw.rect(self.screen, path, pygame.Rect(x_coord, y_coord, 30, 30)) 
            pygame.display.update()
            time.sleep(.05)
            
        #pygame.display.flip()
    #depth first search
    def dfs(self, graph, start, goal):
        stack = [(start, [start])]
        print(type(stack))
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    stack.append((neighbor, path + [neighbor]))


def main():
    start_end= [] #This tells us the start and end indices
    end= [255, 0, 0]
    send_ind=0   #this tells me when I should reset the start and end blocks
    Gindice=0  #this tells me the indice of the start block
    Eindice = 0  #this tells me the idnice of the end block
    green = [0,255, 0]
    wall_indice = {}  #this tells me which block indices are a wall
    button_ind=0  #this tells us if mouse button is up or down for each event
    FPS_CLOCK = pygame.time.Clock()
    grid = Grid()   
    grid.setup_blocks()   #creates a grid 600x600
    running =True    
    while running:    #checks each event and see if it should quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    running = False
            elif (event.type == pygame.QUIT):
                return
            
            if event.type == pygame.MOUSEBUTTONUP : #if the mouse button has been release, then set button_ind =0
                button_ind=0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #if button pushed down, then set button_ind=1
               
                button_ind=1
                position = pygame.mouse.get_pos() #we want the coords of where button was pushed down to display wall
                indice = grid.build_wall(position)
                wall_indice[indice]=1

                
            elif event.type == pygame.MOUSEMOTION and button_ind==1: #if mouse is in motion and button ind==1, which
                                                                     #means button is still down, then find the position
                                                                     #of cursor
                position = pygame.mouse.get_pos()
                indice = grid.build_wall(position)
                wall_indice[indice]=1

            

            #this means that if we click right click for the third time, reset the start/end blocks
            if send_ind==2 and event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
                new_pos= pygame.mouse.get_pos()#find the current position of mouse
                newx_indice = new_pos[0]//30 #to find the left coords of current position of current block your in
                newy_indice = new_pos[1]//30 #to find the top coords of current position of current block your in
                new_indice = 20*newy_indice + newx_indice #calculates the indice you are currently in
                if new_indice not in wall_indice: #if we right click not on a wall block, procede
                    send_ind= 0
                    start_end.remove(Gindice)
                    start_end.remove(Eindice)
                    pygame.draw.rect(grid.screen, grid.gray, pygame.Rect(Gx_indice*30, Gy_indice*30, 30, 30)) 
                    pygame.draw.line(grid.screen , grid.line_color, (Gx_indice*30, Gy_indice*30), (Gx_indice*30+ 30, Gy_indice*30) )
                    pygame.draw.line(grid.screen , grid.line_color, (Gx_indice*30, Gy_indice*30), (Gx_indice*30 , Gy_indice*30+30) )
                    pygame.draw.line(grid.screen , grid.line_color, (Gx_indice*30 +30, Gy_indice*30+30), (Gx_indice*30+30, Gy_indice*30-30))
                    pygame.draw.line(grid.screen , grid.line_color, (Gx_indice*30 +30, Gy_indice*30+30), (Gx_indice*30 - 30 , Gy_indice*30+30))
                    Gindice = 0
                    pygame.draw.rect(grid.screen, grid.gray, pygame.Rect(Ex_indice*30, Ey_indice*30, 30, 30)) 
                    pygame.draw.line(grid.screen , grid.line_color, (Ex_indice*30, Ey_indice*30), (Ex_indice*30+ 30, Ey_indice*30) )
                    pygame.draw.line(grid.screen , grid.line_color, (Ex_indice*30, Ey_indice*30), (Ex_indice*30 , Ey_indice*30+30) )
                    pygame.draw.line(grid.screen , grid.line_color, (Ex_indice*30 +30, Ey_indice*30+30), (Ex_indice*30+30, Ey_indice*30-30))
                    pygame.draw.line(grid.screen , grid.line_color, (Ex_indice*30 +30, Ey_indice*30+30), (Ex_indice*30 - 30 , Ey_indice*30+30))
                    Eindice=0
            #first time we right click, if what we right click is not a wall, then set the start block with a green block
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==3 and send_ind==0:
                posG = pygame.mouse.get_pos()
                Gx_indice = posG[0]//30
                Gy_indice = posG[1]//30
                Gindice = 20*Gy_indice+Gx_indice
                if Gindice not in wall_indice:
                    start_end.append(Gindice) #appends the green indice
                    send_ind=1
                    pygame.draw.rect(grid.screen, green, pygame.Rect(Gx_indice*30, Gy_indice*30, 30, 30)) # draw rectangle of current block
                    pygame.display.flip()
            #for the second time we click, this sets the end block to where we clikced 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button==3 and send_ind==1:
                posE = pygame.mouse.get_pos()
                Ex_indice = posE[0]//30
                Ey_indice = posE[1]//30
                Eindice = 20*Ey_indice+Ex_indice
                if Eindice not in wall_indice:
                    start_end.append(Eindice) #appends end indice
                    send_ind=2
                    pygame.draw.rect(grid.screen, end, pygame.Rect(Ex_indice*30, Ey_indice*30, 30, 30)) # draw rectangle of current block
                    pygame.display.flip()

            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b and len(start_end)==2:
                shortest_path= grid.bfs(grid.neighbors_list, start_end[0], start_end[1]) #call bfs based on start and end block
                if shortest_path != None and start_end[0]!=start_end[1] :  #there must be a path and the start and end block have to be in different indices
                    shortest_path.pop(0) #dont want to highlight start box
                    shortest_path.pop(-1) #dont want to highlight end box
                    for i in shortest_path: #add the path to walls so path act as walls
                        wall_indice[i]=1
                        for x in grid.neighbors_list[i]:
                            if i in grid.neighbors_list[x]:
                                grid.neighbors_list[x].remove(i)
                    grid.draw_path(shortest_path) #draws path
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d and len(start_end)==2:
                path = grid.dfs(grid.neighbors_list, start_end[0], start_end[1]) #call dfs
                if path != None and start_end[0]!=start_end[1] :  #there must be a path and start and end block must not be in the same indice
                    path.pop(0) #dont wanna highlight start block
                    path.pop(-1) #dont wanna highlight end block
                    for i in path: #add path as a wall
                        wall_indice[i]=1
                        for x in grid.neighbors_list[i]:
                            if i in grid.neighbors_list[x]:
                                grid.neighbors_list[x].remove(i)
                    grid.draw_path(path) #draw path

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                start_end= [] #This tells us the start and end indices
                end= [255, 0, 0]
                send_ind=0   #this tells me when I should reset the start and end blocks
                Gindice=0  #this tells me the indice of the start block
                Eindice = 0  #this tells me the idnice of the end block
                green = [0,255, 0]
                wall_indice = {}  #this tells me which block indices are a wall
                button_ind=0  #this tells us if mouse button is up or down for each event
                grid = Grid()   
                grid.setup_blocks()

        FPS_CLOCK.tick(100)
        pos = pygame.mouse.get_pos() #finds the coords of the current cursor postion
        x_indice = pos[0]//30 #to find the left coords of current position of current block your in
        y_indice = pos[1]//30 #to find the top coords of current position of current block your in
        indice = 20*y_indice + x_indice
        #if we havent clicked on a button, we're not on a wall indice, and indice is not a start or end indice, highlight
        if button_ind ==0 and indice not in wall_indice and indice not in start_end: 
            grid.highlight_box(pos) #calls the method according to current position, highlights the current box
        
    return

main()