import pygame
import random
import numpy as np
import math

pygame.init()

WIDTH, HEIGHT = 600,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Simulation")
WHITE= (255,255,255)
T = 4

class Grid:
    def __init__(self):
        self.grid=np.zeros((WIDTH*2,HEIGHT+T))
        self.position=[]
    
    def addSand(self,pointX, pointY):
        if pointX>=0 and pointX<=WIDTH and pointY>=0 and pointY<=HEIGHT:
            if self.grid[pointX][pointY]==0:
                self.grid[pointX][pointY]=1
                self.position.append((pointX,pointY))
                
    def update_position(self):
        for points in self.position:
            listpoints = list(points)
            self.position.remove(points)

            if points[1] >= HEIGHT - T:
                self.position.append(points)
            
            elif self.grid[points[0]][points[1] + T] == 0:
                self.grid[points[0]][points[1]] = 0
                self.grid[points[0]][points[1] + T] = 1
                listpoints[1] += T
                points = tuple(listpoints)
                self.position.append(points)
            
            elif self.grid[points[0]][points[1] + T] == 1:
                if (self.grid[points[0] + T][points[1] + T] == 1) and (self.grid[points[0] - T][points[1] + T] == 1):
                    self.position.append(points)
                    
                elif (self.grid[points[0] + T][points[1] + T] == 1) and (self.grid[points[0] - T][points[1] + T] == 0):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] - T][points[1] + T] = 1
                    listpoints[0] -= T
                    listpoints[1] += T
                    points = tuple(listpoints)
                    self.position.append(points)
                    
                elif (self.grid[points[0] + T][points[1] + T] == 0) and (self.grid[points[0] - T][points[1] + T] == 1):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] + T][points[1] + T] = 1
                    listpoints[0] += T
                    listpoints[1] += T
                    points = tuple(listpoints)
                    self.position.append(points)
                    
                else:
                    self.grid[points[0]][points[1]] = 0
                    a = random.randint(0, 1)
                    if a == 0:
                        a = -1
                    self.grid[points[0] + a * T][points[1] + T] = 1
                    listpoints[0] += a * T
                    listpoints[1] += T
                    points = tuple(listpoints)
                    self.position.append(points)

    
    def draw(self, screen):
        for points in self.position:
            SAND_COLOR=(244,244,255)
            pygame.draw.rect(screen, SAND_COLOR, (points[0],points[1],T,T), 0)       
            # pygame.draw.circle(screen, SAND_COLOR, (points[0],points[1]) , T,3, 0)
                    
                    
    
        


def main():
    run= True
    clock= pygame.time.Clock()
    
    sandbox= Grid()
    while run:
        clock.tick(80)
        screen.fill((25,25,100))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
            
            elif pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                btn=pygame.mouse
                sandbox.addSand(pos[0]-pos[0]%T,pos[1]-pos[1]%T)
        
        sandbox.update_position()
        sandbox.draw(screen)
        
                
               
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()
            