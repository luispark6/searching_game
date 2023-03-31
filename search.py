from operator import truediv
from os import environ
from re import L
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


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






def main():
    grid = Grid()   
    grid.setup_blocks()   #creates a grid 600x600
    print(grid.neighbors_list)
    running =True    
    while running:    #checks each event and see if it should quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    running = False
        
        pos = pygame.mouse.get_pos() #finds the coords of the current cursor postion
        grid.highlight_box(pos) #calls the method according to current position, highlights the current box
        



                

                    
            
            
            



    
    
    


    
    

    

 





main()