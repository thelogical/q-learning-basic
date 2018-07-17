import pygame
import time
from qlearn import Q
import random
import pickle

with open('/home/Cryptik/Desktop/q_values2.pkl', 'rb') as input:
    old_values = pickle.load(input)


pygame.init()

height = 600
width = 800

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('q learning')
clock = pygame.time.Clock()


game_grid = [[0,1,2,3,4,5,6,7,8],
             [9,10,11,12,13,14,15,16,17],
             [18,19,20,21,22,23,24,25,26]]

pits = [0,4,17,19,23]

goals = [6,14,20,25]

class state:
    count = 0

    def __init__(self, x, y, v):
        self.start_x = x
        self.start_y = y
        self.value = v
        self.width = 70
        self.height = 100
        state.count += 1

    def show(self):
        print(str(self.start_x) + " " + str(self.start_y) + " " + str(self.value) + "\n")


class agent:
    def __init__(self):
        self.x = None
        self.y = None

    def moveTo(self, st):
        self.x = 50 + (st%9) * 70 + 35
        self.y = 200 + 80 + int(st/9)*100
        pygame.draw.circle(gameDisplay, (230, 0, 0), [self.x, self.y], 5)

    def erase(self):
        pygame.draw.circle(gameDisplay, (0, 0, 0), [self.x, self.y], 5)


def do_action(index,cur):
    if(index == 0):
        return cur - 1
    elif(index == 1):
        return cur - 9
    elif(index == 2):
        return cur + 1
    else:
        return cur + 9


def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, x, y,size,color):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText,color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)


def draw(State_list):
    for x in State_list:
        vl = x.value
        pygame.draw.rect(gameDisplay, (255, 255, 255),
                         [x.start_x, x.start_y, x.width, x.height], 5)
        message_display(str(vl), x.start_x + x.width / 2, x.start_y + x.height / 2,20,(0,255,0))



def initialize():
    # pygame.draw.rect(gameDisplay,(255,255,255),[100,250,500,100])
    State_list = []
    for row in game_grid:
        for val in row:
            State_list.append(state(50 + row.index(val) * 70, 200 + game_grid.index(row) * 100, val))
    draw(State_list)
    for x in pits:
        for st in State_list:
            if(st.value == x):
                message_display('PIT',st.start_x + 35,st.start_y + 70,10,(255, 182, 0))
    for x in goals:
        for st in State_list:
            if(st.value == x):
                message_display('GOAL',st.start_x + 35,st.start_y + 70,10,(255, 182, 0))
    pygame.display.update()

initialize()

gameExit = False

Ag = agent()

rate = 0.9
discount = 0.3


for ep in range(0,5000):
    end = False
    ok = False
    while not ok:
        cur = random.choice(random.choice(game_grid))
        if(cur not in goals and cur not in pits):
            ok = True
    while not end:
        Ag.moveTo(cur)
        pygame.display.update()
        ind = old_values.Q_values[cur].index(max(old_values.Q_values[cur]))
        if (cur in pits or cur in goals):
            end = True
            Ag.moveTo(cur)
            clock.tick(1)
            Ag.erase()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        cur = do_action(ind, cur)
        Ag.erase()
        clock.tick(1)

pygame.quit()