# -*- coding: utf-8 -*-
"""
Line Bisection Task

Inselspital Bern
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""
from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import random

# get the standard argument parser
parser = ben_tools.getStandardOptions()

# add experiment specific options
parser.add_argument("-n", "--trials", dest="max_trials", type=int, help="define maximum number of trials", 
                  default=40)
                  
# get command line options
options = parser.parse_args()

# process arguments (overwrite false flag_test if filename given)
if options.filename is not None:
    options.flag_save = True
    options.filename = 'output_lb_' + options.filename
else:
    options.filename = 'output_lb_test'

# line parameters
min_length = 0.7
max_length = 1.2

print "variable is a %s" % (options.filename)

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
    
    # start a trial clock
    trial_clock = core.Clock()       
    
    # wait for a button press (NOTE: listener for mouse event)
    myMouse = event.Mouse(win=myWin, visible=True)
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        
        if mouse1:

            # get the position of the click
            click_position = myMouse.getPos()

            # check if click is within reason or ignore           
            if abs(click_position[0] - position[0]) < 0.4 and \
            abs(click_position[1] - position[1]) < 0.2:
                
                # compute distance to line center
                estimate = position[0] - click_position[0]

                print "you were %.2f off the target" % (estimate)               
                
                # draw the estimate               
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
                
                # let the line sit on the screen a second
                core.wait(0.5)
    
                return estimate, trial_clock.getTime()

            # if the user clicks the bottom right it exits the program
            elif click_position[0] > 0.9 and \
            click_position[1] < -0.9:
                return 2, 0
                        
        elif mouse3:
            return 2, 0
                    

# initialise experiment
# prepare experiment data to save
data_out = data.ExperimentHandler(name='line bisection', 
                                  version='alpha', 
                                  dataFileName=options.filename,
                                  savePickle=options.flag_save,
                                  saveWideText=options.flag_save)
                                  
# open a new window
# myWin = visual.Window(fullscr=1, color=[1, 1, 1], monitor="testMonitor", units="degs")
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=1, monitor="testMonitor", units="norm")
event.Mouse(visible=False)

# hit next to continue text
message1 = visual.TextStim(win=myWin,
                           alignHoriz='center',
                           alignVert='center', 
                           color=(0, 0, 0),
                           colorSpace='rgb',
                           units='', 
                           pos=[0,0],
                           text='Druecken Sie eine Taste\num anzufangen')

# put the message on the screen
message1.draw()   
myWin.flip()                   
# wait for touch    
ben_tools.waitForClick(myWin)

# run trials until 
trial_count = 0
while trial_count < options.max_trials:
    
    # get random values for position and length
    line_length = random.uniform(min_length, max_length)
    
    # position boundaries depends on line length
    position = []
    max_x = 0.95 - max_length / 2
    position.append(random.uniform(-max_x, max_x))
    position.append(random.uniform(-0.7, 0.7))
    
    # run the task 
    estimate, trial_time = lineBisectionTask(line_length, position)  
    
    if estimate is 2:
        break

    # save the parameters
    data_out.addData('x_pos', position[0])
    data_out.addData('y_pos', position[1])
    data_out.addData('length', line_length)
    data_out.addData('error', estimate)
    data_out.addData('time', trial_time)
    
    # go to next trial in the loop
    data_out.nextEntry()    

    # advance trial counter
    trial_count = trial_count + 1

# wait 500ms and close the screen
core.wait(0.5)

myWin.close()
core.quit