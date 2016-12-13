# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 23:01:57 2016

@author: mensen
"""

from psychopy import event  # import some libraries from PsychoPy


def waitForClick(myWin):
    
    # define mouse
    myMouse = event.Mouse(win=myWin, visible=True)    
    
    while True:
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
    
        if mouse1:
            return 1
        if mouse3:
            return 255