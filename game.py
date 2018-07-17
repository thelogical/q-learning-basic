import pygame
import time

pygame.init()

class state:
    count = 0
    def __init__(self,x,y,v):
        self.start_x = x
        self.start_y = y
        self.value = v
        self.width = 70
        self.height = 100
        state.count += 1

    def show(self):
        print(str(self.start_x)+" "+str(self.start_y)+" "+str(self.value)+"\n")

class agent:
    def __init__(self):
        self.x = None
        self.y = None

    def moveTo(self,st):
        self.x = 50+st*50+35
        self.y = 250+80
        pygame.draw.circle(gameDisplay,(100,200,150),[self.x,self.y],5)


gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('q learning')
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, (0,200,0))
    return textSurface, textSurface.get_rect()

def message_display(text,x,y):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

def draw(State_list):
    for x in State_list:
        vl = x.value
        pygame.draw.rect(gameDisplay, (255-vl*20, 255-vl*20, 255-vl*20), [x.start_x, x.start_y, x.width, x.height],5)
        message_display(str(vl),x.start_x+x.width/2,x.start_y+x.height/2)

def initialize():
    #pygame.draw.rect(gameDisplay,(255,255,255),[100,250,500,100])
    State_list = []
    for x in range(0,10):
        State_list.append(state(50 + x*70,250,x))
    draw(State_list)
    pygame.display.update()

def initialize_agent():
    cur = 2
    #Ag = agent()
    #Ag.moveTo(cur)



initialize()

initialize_agent()

gameExit = False

while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
