import pygame
import time
from qlearn import Q
import random
import pickle


pygame.init()

height = 600
width = 800

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('q learning')
clock = pygame.time.Clock()


game_grid = [[0,1,2,3,4,5,6,7,8],
             [9,10,11,12,13,14,15,16,17],
             [18,19,20,21,22,23,24,25,26]]

pits = [0,4,12,17,19,23]

goals = [6,14,20,25]

rewards = [
           [None, None, 0, 0],
           [-200, None, 0, 0],
           [0, None, 0, 0],
           [0, None, -200, -200],
           [0, None, 0, 100],
           [-200, None, 100, 100],
           [0, None, 0, 0],
           [100, None, 0, 0],
           [0, None, None, -200],
           [None, -200, 0, 0],
           [0, 0, 0, -200],
           [0, 0, -200, 100],
           [0, 0, 0, 0],
           [-200, -200, 100, 0],
           [0, 0, 0, 0],
           [100, 100, 0, 0],
           [0, 0, -200, 100],
           [0, 0, None, 0],
           [None, 0, -200, None],
           [0, 0, 100, None],
           [-200, 0, 0, None],
           [100, -200, 0, None],
           [0 , 0, -200, None],
           [0, 100, 0, None],
           [0, 0, 100, None],
           [0, 0, 0, None],
           [100, -200, None, None]
                   ]

q_values = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
                         ]

transition = [[False, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, True, True],
              [True, False, False, True],
              [False, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, True, True],
              [True, True, False, True],
              [False, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, True, False],
              [True, True, False, False],
                                        ]


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
    cur = random.choice(random.choice(game_grid))
    end = False
    index = -1
    action = False
    print(ep + 1)
    print("\n \n")
    while not end:
        action = False
        Ag.moveTo(cur)
        pygame.display.update()
        next_action = transition[cur]
        while action == False:
            index = random.randint(0,3)
            action = next_action[index]
        next_action = do_action(index,cur)
        q_values[cur][index] = q_values[cur][index] + rate*(rewards[cur][index] + discount*max(q_values[next_action])) - q_values[cur][index]
        cur = next_action
        if (cur in pits or cur in goals):
            end = True
            Ag.erase()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(q_values)
        print("\n")
        Ag.erase()
        #clock.tick(1000)

pygame.quit()

with open('/home/Cryptik/Desktop/q_values.pkl', 'wb') as output:
    lst = Q(q_values)
    pickle.dump(lst, output, pickle.HIGHEST_PROTOCOL)