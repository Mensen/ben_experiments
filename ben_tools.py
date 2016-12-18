# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 23:01:57 2016

@author: mensen
"""

from psychopy import event, visual  # import some libraries from PsychoPy


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
            
def takeABreak(myWin, pause_time):

    message1 = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center', 
           color=(0, 0, 0),
           colorSpace='rgb',
           units='', 
           pos=[0,0],
           text='Zeit fuer eine Pause.')
    
    # put the message on the screen
    message1.draw()   
    myWin.flip()        

    core.wait(pause_time)
    
def pushToContinue(myWin):
    
    message1 = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center', 
           color=(0, 0, 0),
           colorSpace='rgb',
           units='', 
           pos=[0,0],
           text='Druecken Sie eine Taste um fortzufahren.')
    
    # put the message on the screen
    message1.draw()   
    myWin.flip()        
               
    # wait for mousepress
    button = waitForClick(myWin)
    
    