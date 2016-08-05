# -*- coding: utf-8 -*-
"""
Line Bisection Task

Inselspital Bern
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import random

# define functions
def convertToPos(line_length, position):
    vertices=[(position[0] - line_length/2.0, position[1]), (position[0] + line_length/2.0, position[1])]
    return vertices

def lineBisectionTask(line_length, position):
    # create a line
    line_pos=convertToPos(line_length, position)
    myLine = visual.ShapeStim(win=myWin, 
                  units='norm', 
                  vertices=line_pos, 
                  lineColor=[-1, -1, -1], 
                  lineColorSpace='rgb',
                  lineWidth=10)
    
    event.Mouse(visible=True)    
    
    # draw the line on the screen
    myLine.draw()
    myWin.flip()
    
    # wait for a button press
    myMouse = event.Mouse(win=myWin, visible=True)
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        
        if mouse1:

            #check if click is within reason            
            click_position = myMouse.getPos()

            if abs(click_position[0] - position[0]) < 0.2 and \
            abs(click_position[1] - position[1]) < 0.2:
                
                # compute distance to line center
                estimate = position[0] - click_position[0]

                print "you were %.2f off the target" % (estimate)               
                
                # draw the estimate
                # print "variable is a %s" % (type(position[0]))
                marked_pos = [(click_position[0], position[1] + 0.1), (click_position[0], position[1] - 0.1)]
                markedLine = visual.ShapeStim(win=myWin, 
                  units='norm', 
                  vertices=marked_pos,
                  lineColor=[0, 0, 0], 
                  lineColorSpace='rgb')                
               
                # redraw both line and marking
                myLine.draw()
                markedLine.draw()
                myWin.flip()
                
                core.wait(0.5)
    
                return estimate

            # if the user clicks the bottom right it exits the program
            elif click_position[0] > 0.9 and \
            click_position[1] < -0.9:
                
                return 2
                        
        elif mouse3:
            
            return 2
                    

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
# wait for keypress    
event.waitKeys()


# run trials until 
while True:
    # get random values for position and length
    line_length = random.uniform(0.8, 1)
    position = []
    position.append(random.uniform(-0.2, 0.2))
    position.append(random.uniform(-0.6, 0.6))
    
    # run the task 
    estimate = lineBisectionTask(line_length, position)  
    
    if estimate is 2:
        break

    # save the parameters
    data_out.addData('x_pos', position[0])
    data_out.addData('y_pos', position[1])
    data_out.addData('length', line_length)
    data_out.addData('error', estimate)
    
    # go to next trial in the loop
    data_out.nextEntry()    

# wait 500ms and close the screen
core.wait(0.25)

myWin.close()
core.quit