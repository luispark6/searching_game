from operator import truediv
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class Grid:
    width = 600
    height = 600
    blue = [127, 255, 212]

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")
        screen.fill(self.blue)
        pygame.display.flip()
    #def setup_blocks(self):
        #we should display the screen slowly



def main():
    grid = Grid()
    running =True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                    running = False
            



    
    
    


    
    

    

 





main()