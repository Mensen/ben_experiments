# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 23:01:57 2016

@author: mensen
"""

from psychopy import event, visual, core  # import some libraries from PsychoPy
import argparse
import os
import errno

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
         
def welcomeMessage(myWin, text):
    event.Mouse(visible=False)

    # welcome message
    message1 = visual.TextStim(win=myWin,
       alignHoriz='center',
       alignVert='center', 
       color=(0, 0, 0),
       colorSpace='rgb',
       units='', 
       pos=[0,0],
       text=text)
       
    # put the message on the screen
    message1.draw()   
    myWin.flip()                   
    # wait for keypress    
    core.wait(2)
    
    # welcome message
    message1 = visual.TextStim(win=myWin,
       alignHoriz='center',
       alignVert='center', 
       color=(0, 0, 0),
       colorSpace='rgb',
       units='', 
       pos=[0,0],
       text='Druecken Sie eine Taste um fortzufahren')
       
    # put the message on the screen
    message1.draw()   
    myWin.flip()
             
    # wait for mousepress
    waitForClick(myWin)         
         
def takeABreak(myWin, pause_time):

    message1 = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center', 
           color=(0, 0, 0),
           colorSpace='rgb',
           units='', 
           pos=[0,0],
           text='Super! Zeit fuer eine Pause.')
    
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
    waitForClick(myWin)
  
def showEnd(myWin):
    
    # draw end text
    cross_object = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center',
           units='norm',
           height=0.6,           
           color=(0, 0, 0),
           colorSpace='rgb',
           pos=[0,0],
           text='Danke!')
           
    # put the image on screen
    cross_object.draw()
    myWin.flip() 
  
def getStandardOptions():
    # initiate the parser object
    parser = argparse.ArgumentParser()
    
    # add the default values
    parser.add_argument("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_argument("-s", action="store_true", dest="flag_save", default=False,
                      help="boolean flag for saving data to file")
                      
    return parser
    
def checkDirectory(directory_name):
    try:
        os.makedirs(directory_name)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise