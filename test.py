import time
import random
from qlearn import Q
import random
import pickle


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
           [0 , 0, 100, None],
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


def converge(v1,v2):
    if(abs(v1-v2) < 1e-7):
        return True
    else:
        return False

def do_action(index,cur):
    if(index == 0):
        return cur - 1
    elif(index == 1):
        return cur - 9
    elif(index == 2):
        return cur + 1
    else:
        return cur + 9


def loop(rate,discount,eps):
    for ep in range(0,eps):
        cur = random.choice(random.choice(game_grid))
        end = False
        index = -1
        action = False
        #print(ep + 1)
        #print("\n \n")
        while not end:
            action = False
            next_action = transition[cur]
            while action == False:
                index = random.randint(0, 3)
                action = next_action[index]
            next_action = do_action(index, cur)
            q_values[cur][index] = q_values[cur][index] + rate * (
                    rewards[cur][index] + discount * max(q_values[next_action])) - q_values[cur][index]
            cur = next_action
            if (cur in pits or cur in goals):
                end = True
                break

            if(ep >= 10):
                with open('/home/Cryptik/Desktop/q_values.pkl', 'rb') as input:
                    old_values = pickle.load(input)
                    fl = 0
                    for r1, r2 in zip(q_values, old_values.Q_values):
                        for c1, c2 in zip(r1, r2):
                            if (c1 == 0 and c2 == 0):
                                continue
                            if not converge(c1,c2):
                                print(c1,c2)
                                fl = 1
                    if(fl == 0):
                        print("complete at",ep + 1)
                        break
                    fl = 0


            with open('/home/Cryptik/Desktop/q_values.pkl', 'wb') as output:
                lst = Q(q_values)
                pickle.dump(lst, output, pickle.HIGHEST_PROTOCOL)