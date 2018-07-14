import pygame
import time
import random


pygame.init()

height = 600
width = 800

window = pygame.display.set_mode((width,height))

pygame.display.set_caption('Q-learning')

clock = pygame.time.Clock()


start_states = [1,2,3,4,5,7,8,9]

states = [0,1,2,3,4,5,6,7,8,9]

rewards = [[None,0],
           [-100,0],
           [0,0],
           [0,0],
           [0,0],
           [0,100],
           [0,0],
           [100,0],
           [0,0],
           [0,None]]

q_values = [[0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0]]

end_states = [0,6]



def do_action(index,cur):
    if(index == 0):
        return cur - 1;
    else:
        return cur + 1;

def get_next_action(cur):
    for x in states:
        if(x == cur):
            if(x == 0):
                return [False,True]
            elif (x == 9):
                return [True,False]
            else:
                return [True,True]

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

    def erase(self,sts):
        for x in sts:
            pygame.draw.circle(gameDisplay, (0, 0, 0), [50 + x*70 + 35, 250+80], 5)

    def moveTo(self, st):
        self.x = 50 + st * 70 + 35
        self.y = 250 + 80
        self.erase(states)
        pygame.draw.circle(gameDisplay, (230, 0, 0), [self.x, self.y], 5)
        pygame.display.update()







gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('q learning')
clock = pygame.time.Clock()


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
        pygame.draw.rect(gameDisplay, (255 - vl * 20, 255 - vl * 20, 255 - vl * 20),
                         [x.start_x, x.start_y, x.width, x.height], 5)
        message_display(str(vl), x.start_x + x.width / 2, x.start_y + x.height / 2,20,(0,255,0))


def initialize():
    State_list = []
    for x in states:
        State_list.append(state(50 + x * 70, 250, x))
    draw(State_list)
    message_display('PIT',50 + 35,270,10,(255, 182, 0))
    message_display('GOAL',50 + 6 * 70 + 35,270,10,(255, 182, 0))
    pygame.display.update()


initialize()

gameExit = False

Ag = agent()

for ep in range(0,10):
    Ag.erase(states)
    pygame.display.update()
    cur = random.choice(start_states)
    end = False
    index = -1
    rate = 1 - 0.9
    discount = 0.2
    action = False
    print(ep)
    print("\n \n")
    while not end:
        action = False
        Ag.moveTo(cur)
        next_action = get_next_action(cur)
        while action == False:
            index = random.randint(0,1)
            action = next_action[index]
        next_action = do_action(index,cur)
        q_values[cur][index] = q_values[cur][index] + rate*(rewards[cur][index] + discount*max(q_values[next_action])) - q_values[cur][index]
        cur = next_action
        if (cur in end_states):
            end = True
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(q_values)
        print("\n")
        clock.tick(10)

pygame.quit()