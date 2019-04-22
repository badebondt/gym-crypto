#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 13:53:45 2019

@author: bavodebondt
"""


import gym
from gym import error, spaces, utils
from gym.utils import seeding

import glob
import os
import random

import pandas as pd
import numpy as np

ACTION_SKIP = 0
ACTION_BUY = 1
ACTION_SELL = 2

class StockState:
    
    def reset(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.df) - 1:
            return None, True

        values = self.df.iloc[self.index].values

        self.index += 1

        return values, False

    def shape(self):
        return self.df.shape

    def current_price(self):
        return self.dfclose.ix[self.index, 'Close']

class CryptoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, datadir):

        self.comission = 0.35/ 100.
        self.spread = 2/100.
        #self.num = 1
        self.money = 0
        self.equity = 0
        self.seed()
        self.states = []
        self.state = None

        #for path in glob.glob(datadir + '/*.csv'):
         #   if not os.path.isfile(path):
          #      continue

           # self.states.append(path)
       
        high = np.array([
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max])
        
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        #self.observation_space = spaces.Box(low=0, high=self.bound, shape=(13,1))
        self.action_space = spaces.Discrete(3)
        
        if len(self.states) == 0:
            raise NameError('Invalid empty directory {}')

        
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
        
    def step(self, action):
        assert self.action_space.contains(action)
        price = self.state.current_price()
        portfolio = self.money + self.equity * self.state.current_price()
        num = portfolio/(price*(1+self.comission + self.spread))
        cost = price * num
        
        comission_price = cost * (1. + self.comission + self.spread)
        equity_price = price * self.equity
        prev_portfolio = self.money + equity_price

        if action == ACTION_BUY:
            if self.money >= comission_price:
                self.money -= comission_price
                self.equity += self.num
                
        if action == ACTION_SELL:
            if self.equity > 0:
                self.money += (1. - self.comission - self.spread) * cost
                self.equity -= self.num

        state, done = self.state.next()

        new_price = price
        if not done:
            new_price = self.state.current_price()

        new_equity_price = new_price * self.equity
        reward = (self.money + new_equity_price) - prev_portfolio

        return state, reward, done, None
    
        self.states.append(state)        

    def reset(self):
        self.state = StockState(random.choice(self.states))

        self.money = 1000000
        self.equity = 0

        state, done = self.state.next()
        return state

    def _render(self, mode='human', close=False):
        pass
