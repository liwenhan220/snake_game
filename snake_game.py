import numpy as np
import cv2
from collections import deque
import time
from PIL import Image
from getkeys import key_check

class snake_game:
    def __init__(self):
        self.size = 40
        self.subject = (0, 0, 255)
        self.food = (0, 255, 0)
        self.segment = (0,0,255)
        self.total_reward = 0
        

    def init_game(self):
        self.img = np.zeros((self.size,self.size,3))
        return self.img
    
    def reset(self):
        self.sub_x = int(self.size/2)
        self.sub_y = int(self.size/2)
        self.food_x = np.random.randint(0,self.size)
        self.food_y = np.random.randint(0,self.size)        
        self.img = self.init_game()
        self.img[self.sub_x][self.sub_y] = self.subject
        self.img[self.food_x][self.food_y] = self.food
        self.reward = 0
        self.total_reward = 0
        self.segments = []
        
        return self.img
    
    def update_frame(self):
        self.img = np.zeros((self.size,self.size,3))
        self.img = self.init_game()
        self.img[self.sub_x][self.sub_y] = self.subject
        self.img[self.food_x][self.food_y] = self.food
        try:
            for i in range(len(self.segments)):
                self.img[self.segments[i][0]][self.segments[i][1]] = self.segment
        except:
            pass
                                              
        return self.img

    def step(self,input_n):
        
        self.segments.append([self.sub_x,self.sub_y])
        if len(self.segments) > self.total_reward:
            del self.segments[:(len(self.segments)-self.total_reward)]

        # moving left
        if input_n == 0:
            self.sub_x -= 1
            
        # moving right
        elif input_n == 1:
            self.sub_x += 1
            
        # moving down
        elif input_n == 2:
            self.sub_y -= 1
            
        # moving up
        elif input_n == 3:
            self.sub_y += 1
            
        if self.sub_x > self.size-1 or self.sub_x < 0 or self.sub_y < 0 or self.sub_y > self.size-1:
            self.terminal = True
            self.reward = -1
            
        elif self.food_x - self.sub_x == 0 and self.food_y - self.sub_y == 0:
            self.terminal = False
            self.reward = 1
            self.food_x = np.random.randint(0,self.size)
            self.food_y = np.random.randint(0,self.size)
            self.img = self.update_frame()    
        else:
            self.terminal = False
            self.reward = 0
            self.img = self.update_frame()
            
        for i in range(len(self.segments)):
            if self.sub_x == self.segments[i][0] and self.sub_y == self.segments[i][1]:
                self.terminal = True
                self.reward = -1
                return self.img, self.reward, self.terminal

        if self.reward == 1:
            self.total_reward += self.reward

        return self.img, self.reward, self.terminal

env = snake_game()


for i in range(100):
    last_action = 1
    state = env.reset()
    done = False
    while not done:
        time.sleep(0.01)
        
        keys = key_check()
        if 'W' in keys:
            action = 0
        elif 'S' in keys:
            action = 1
        elif 'A' in keys:
            action = 2
        elif 'D' in keys:
            action = 3
        else:
            action = last_action
            
        
        state, reward, done = env.step(action)
        cv2.imshow('w',cv2.resize(state,(300,300)))
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        last_action = action

