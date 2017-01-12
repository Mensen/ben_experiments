# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 00:00:58 2016

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
from ben_tools import waitForClick
import numpy as np
import os

# experiment parameters
number_of_trials = 1

# available images
images = [os.path.join("rsc_images", "rsc_bw.png")]

def objectSelect(current_image):
    # prepare the image
    rsc_image.setImage(current_image)
    rsc_image.draw(myWin)
    
    # put the image on screen
    myWin.flip()
    
    event.Mouse(visible=True)    
    # wait for a button press
    myMouse = event.Mouse(win=myWin, visible=True)
    
    position_x=[]
    position_y=[]
    
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()

        if mouse1:
            # get the position of the click
            click_position = myMouse.getPos()
             
            position_x.append(click_position[0])
            position_y.append(click_position[1])         
             
            # prepare some text
            marking = visual.TextStim(win=myWin,
                   alignHoriz='center',
                   alignVert='center', 
                   color=(0, 0, 0),
                   colorSpace='rgb',
                   units='', 
                   pos=[click_position[0], click_position[1]],
                   text='X')
            marking.autoDraw=True
            
            # put the x image on screen
            myWin.flip()
            core.wait(0.5)

        
        # exit on right mouse button        
        if mouse3:
            
            # clear the screen
            rsc_image.autoDraw=False
            myWin.flip()
            
            return position_x, position_y

# prepare experiment data to save
data_out = data.ExperimentHandler(name='line bisection', 
      version='alpha', 
      dataFileName='output_rsc')

# open a new window
myWin = visual.Window( 
    color=[1, 1, 1], 
    fullscr=1, 
    monitor="testMonitor", 
    units="norm")
    
rsc_image = visual.ImageStim(myWin,
    units='norm',
    size=[2, 2])
rsc_image.autoDraw=True
    
# run the experiment
for n_trial in range(0, number_of_trials):
    position_x, position_y = objectSelect(images[n_trial])

    # save the parameters
    data_out.addData('position_x', position_x)
    data_out.addData('position_y', position_y)

    # go to next trial in the loop
    data_out.nextEntry()   
    
# wait for mousepress
button = waitForClick(myWin)

# wait 500ms and close the screen
core.wait(0.5)
myWin.close()
core.quit