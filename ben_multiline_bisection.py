# -*- coding: utf-8 -*-
"""
Multi-Line Bisection Task

Inselspital Bern
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
from ben_tools import waitForClick
import random
import numpy as np

# define functions
def convertToPos(line_length, position):
    vertices=[(position[0] - line_length/2.0, position[1]), \
    (position[0] + line_length/2.0, position[1])]
    return vertices

def multiLineBisectionTask(line_length, position_x, position_y):
    
    # pre-allocation step
    myLine = number_of_lines*[None]
    markedLine = number_of_lines*[None]
    
    # set flag for marked lines 
    flag_marked = np.ones((number_of_lines, 1), dtype=bool)    
    
    # create lines
    for n_line in range(0, number_of_lines):
        line_pos=convertToPos(line_length[n_line], \
        [position_x[n_line], position_y[n_line]])
        myLine[n_line] = visual.ShapeStim(win=myWin, 
              units='norm', 
              vertices=line_pos, 
              lineColor=[-1, -1, -1], 
              lineColorSpace='rgb',
              lineWidth=10)
              
        # set to always draw after flips
        myLine[n_line].setAutoDraw(True) 
    
    # show the mouse
    event.Mouse(visible=True)    
    
    # draw the line on the screen
    myWin.flip()
    
    estimate = number_of_lines*[None]  
    counter = 0    
    
    # wait for a button press
    myMouse = event.Mouse(win=myWin, visible=True)
    while counter < number_of_lines:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        
        if mouse1:
            # get the position of the click
            click_position = myMouse.getPos()

            # figure out which line was clicked on
            distance_to_line = position_y - click_position[1]
            line_index = (np.abs(distance_to_line)).argmin()

            #check if click is within reason or ignore           
            if abs(click_position[0] - position_x[line_index]) < 0.4 and \
            abs(click_position[1] - position_y[line_index]) < 0.2 and \
            flag_marked[line_index]:
                
                # compute distance to line center
                estimate[counter] = position_x[line_index] - click_position[0]
                print "you were %.3f off the target" % (estimate[counter])               
                
                # draw the estimate
                # print "variable is a %s" % (type(position[0]))
                marked_pos = [(click_position[0], position_y[line_index] + 0.1), \
                (click_position[0], position_y[line_index] - 0.1)]
                
                markedLine[counter] = visual.ShapeStim(win=myWin, 
                  units='norm', 
                  vertices=marked_pos,
                  lineColor=[0, 0, 0], 
                  lineColorSpace='rgb',
                  autoDraw=True)                

                # mark the line bisection as complete
                flag_marked[line_index] = False

                # update line counter
                counter += 1               
               
                # draw marking
                myWin.flip()
                    
            # if the user clicks the bottom right it exits the program
            elif click_position[0] > 0.9 and \
            click_position[1] < -0.9:

                # exit the block and trial with error code "2"
                return 2
                        
        elif mouse3:
            
            return 2
 
    # clear the autodraw objects
    for n in range(0, number_of_lines):
        myLine[n].setAutoDraw(False)
        markedLine[n].setAutoDraw(False)
    
    # return from the function with all the estimates    
    return estimate
                  

# initialise experiment
# prepare experiment data to save
data_out = data.ExperimentHandler(name='line bisection', 
                                  version='alpha', 
                                  dataFileName='output_lb')
                                  
# open a new window
# myWin = visual.Window(fullscr=1, color=[1, 1, 1], monitor="testMonitor", units="degs")
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=1, monitor="testMonitor", units="norm")
event.Mouse(visible=False)

# prepare some text
message1 = visual.TextStim(win=myWin,
       alignHoriz='center',
       alignVert='center', 
       color=(0, 0, 0),
       colorSpace='rgb',
       units='', 
       pos=[0,0],
       text='Hit a key when ready.')

# put the message on the screen
message1.draw()   
myWin.flip()        
           
# wait for mousepress
button = waitForClick(myWin)

# define maximum number of trials
max_trials = 2
number_of_lines = 8

min_length = 0.7
max_length = 1.2
x_boundary = 0.98 - max_length / 2

# run trials until 
trial_count = 0
while trial_count < max_trials:
    
    # make the lines
    line_length = number_of_lines*[None]  
    position_x = number_of_lines*[None] 
    
    for n in range(0, number_of_lines):
        # get random values for position and length
        line_length[n] = random.uniform(min_length, max_length)
        position_x[n] = random.uniform(-x_boundary, x_boundary)
        
    # y position is even spread over range    
    position_y = np.linspace(-0.8, 0.8, num = number_of_lines) + random.uniform(-0.03, 0.03)
    
    # run the task 
    estimate = multiLineBisectionTask(line_length, position_x, position_y)  
    
    if estimate[0] is 2:
        break

    # save the parameters
    data_out.addData('block_number', trial_count + 1)
    data_out.addData('x_pos', position_x)
    data_out.addData('y_pos', position_y)
    data_out.addData('length', line_length)
    data_out.addData('error', estimate)
    
    # go to next trial in the loop
    data_out.nextEntry()    

    # advance trial counter
    trial_count = trial_count + 1

# wait 500ms and close the screen
core.wait(0.5)

myWin.close()
core.quit