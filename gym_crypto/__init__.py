#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 12:34:16 2019

@author: bavodebondt
"""

from gym.envs.registration import register

register(
    id='Crypto-v0',
    entry_point='gym_crypto.envs:CryptoEnv',)
