# -*- coding: utf-8 -*-
"""
Corsi Block Test

Inselspital Bern
Bern Network for Sleep Epilepsy and Consciousness
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import numpy as np
import scipy.spatial.distance
import os

# get the standard argument parser
parser = ben_tools.getStandardOptions()

# add experiment specific options
parser.add_argument("-m", "--mode", dest="mode", help="test mode: classic or scale", 
                  default='classic')
parser.add_argument("-r", "--reverse", dest="flag_reverse", help="test mode: forward or reverse", 
                  action="store_true", default=False) 
parser.add_argument("-t", "--time", dest="display_time", type=float, help="time to display each box during presentation", 
                  default=1.0) 
                  
# get command line options
options = parser.parse_args()

# process arguments (overwrite false flag_test if filename given)
direction = 'n'
if options.flag_reverse:
    direction = 'r'

if options.filename is not None:
    options.flag_save = True
else:
    options.filename = 'test'

# check for results directory
save_path = os.path.join('results', options.filename)
ben_tools.checkDirectory(save_path)

# maximum number of trials
trials_max = 20
# starting number of boxes
num_boxes = 9
num_to_test = 2
max_fails = 3

# basic box background color
fill_color = [0.7, 0.7, 0.7]


def boxCoordinates(centre, size):

    screen_ratio = 14/9.0

    size = size / 2
    
    box_vertices = [ \
    [centre[0] - size / screen_ratio, centre[1] - size], \
    [centre[0] - size / screen_ratio, centre[1] + size], \
    [centre[0] + size / screen_ratio, centre[1] + size], \
    [centre[0] + size / screen_ratio, centre[1] - size] ]
    
    return box_vertices


def getBoxPositions(num_box, box_size):

    #calculate minimum safe distance
    min_dist = 1.0 / num_box + box_size
       
    # check minimum distance for all element pair distances
    while True:
        # generate random positions
        centers = np.random.uniform(-0.8, 0.8, [num_box, 2])   
        
        dist = scipy.spatial.distance.pdist(centers)
        
        if dist.min() > min_dist:
            break

    # allocate vertices array
    box_vertices=num_box*[None]    

    for block in range(0, num_box):
        box_vertices[block] = boxCoordinates(centers[block, :], box_size) 
    
    return box_vertices
  

def checkBox(click_position):
    
    for block in range(0, num_boxes):
        
        if click_position[0] > my_boxes[block].vertices[0][0] and \
            click_position[0] < my_boxes[block].vertices[2][0] and \
            click_position[1] > my_boxes[block].vertices[0][1] and \
            click_position[1] < my_boxes[block].vertices[1][1]:
                    
            return block

    return 100                
    
def makeBlocks(num_box):

    box_size = 0.25

    box_vertices = getBoxPositions(num_box, box_size)

    # allocate objects
    my_boxes = num_box*[None]   
       
    for block in range(0, num_box):     
        
        # draw a block
        my_boxes[block] = visual.ShapeStim(win=myWin, 
                  units='norm', 
                  lineColor=[-1, -1, -1], 
                  lineColorSpace='rgb',
                  vertices = box_vertices[block],
                  fillColor = fill_color,
                  fillColorSpace = 'rgb',
                  lineWidth=5)      

        # set to always draw after flips
        my_boxes[block].setAutoDraw(True)     
                                                 
    # flip the boxes on the screen                  
    myWin.flip()
    #event.waitKeys()
    core.wait(1)
    return my_boxes


def corsiBlockTest(num_to_test):
    
    # pre-allocate trial time
    trial_time = num_to_test * [0]
    missed_hits = 0
    
    for block in range(0, num_to_test):

        my_boxes[block].fillColor = [-1, -1, 1]
        
        myWin.flip()
        
        core.wait(options.display_time)
        
        my_boxes[block].fillColor = fill_color

        myWin.flip()
        
    # start a trial clock
    trial_clock = core.Clock() 
   
    # adjust loop for direction
    loop_range = range(0, num_to_test)
    
    if options.flag_reverse:
        loop_range.reverse()
   
    for block in loop_range:
        # wait for a button press
        myMouse = event.Mouse(win=myWin, visible=True)
        
        # wait for mouse click
        while True:
            
            myMouse.clickReset()
            mouse1, mouse2, mouse3 = myMouse.getPressed()
            
            if mouse1:
                # was it within the correct block?
                myMouse.clickReset()
                click_position = myMouse.getPos()
                                
                trial_time[block] = trial_clock.getTime()               
                
                # check which box was pressed
                clicked_box = checkBox(click_position)                
                
                # make sure click position is within block
                if clicked_box is block:
                    
                    # change to green
                    my_boxes[block].fillColor = [-1, 1 , -1]
                    myWin.flip()
                    # change back to grey (flipped after next click)
                    my_boxes[block].fillColor = fill_color
                    break
                
                elif clicked_box is 100:
                    
                    # xount the times missed the box
                    missed_hits += 1
                    
                    # wait to avoid counting click multiple times
                    core.wait(0.08)
                    
                else:
                    # change all to red
                    for n in range(0, len(my_boxes)):
                        my_boxes[n].fillColor = [1, -1 , -1]
                    myWin.flip()
                                        
                    # exit with 
                    for n in range(0, len(my_boxes)):
                        my_boxes[n].setAutoDraw(False)   
        
                    # show red boxes for a second
                    core.wait(1) 
                    myWin.flip()
                           
                    if options.flag_reverse:
                        trial_time.reverse()
                        block = num_to_test-block
                          
                    return block, trial_time
            
            if mouse3:
                for n in range(0, len(my_boxes)):
                    my_boxes[n].setAutoDraw(False)
        
                myWin.flip() 
                return 255, trial_time     
            
    # if all correct flash all green
    for n in range(0, len(my_boxes)):
        my_boxes[n].fillColor = [-1, 1 , -1]
    myWin.flip()
        
    # erase the squares
    for n in range(0, len(my_boxes)):
        my_boxes[n].setAutoDraw(False)   
        
    core.wait(1)    
    myWin.flip()
    
    # check for reverse condition
    if options.flag_reverse:
        trial_time.reverse()
    
    print('you missed %d times') %(missed_hits)                
    
    return num_to_test, trial_time, missed_hits

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section
# prepare experiment data to save
save_name = os.path.join(save_path, 'output_cb_' + options.filename + '_' + options.mode[0] + '_' + direction)
data_out = data.ExperimentHandler(name='corsi block', 
    version=options.mode, 
    dataFileName=save_name)   

# open a unique window
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=1, monitor="testMonitor", units="norm")

# run the welcomeMessage function
ben_tools.welcomeMessage(myWin, 'Corsi Block Test')

# loop trials
trial = 0
consecutive_fails = 0
while trial < trials_max:
       
    # check for sufficient boxes
    if num_boxes < num_to_test:
        num_boxes = num_to_test
    
    if options.mode in ['scale']:
        # number of boxes adjust to test number
        num_boxes = num_to_test
    
    # draw the boxes on screen
    my_boxes = makeBlocks(num_boxes)   
    
    # test the participant
    flag_correct, trial_time, missed_clicks = corsiBlockTest(num_to_test)

    # exit signal
    if flag_correct == 255:
        break
    
    # print result of trial in the command line
    print('you got %d of %d correct') %(flag_correct, num_to_test) 
    # print('variable is %.2f') %(trial_time[0]) 

    # save the results
    data_out.addData('number_to_test', num_to_test)
    data_out.addData('number_correct', flag_correct)
    data_out.addData('trial_time', trial_time)
    data_out.addData('missed_clicks', missed_clicks)

#    # go to next trial in the loop
    data_out.nextEntry()    

    # process arguments for next trial
    if flag_correct == num_to_test:
        # if correct increase number of boxes
        num_to_test = num_to_test + 1
        # reset fails if correct
        consecutive_fails = 0
    elif flag_correct < num_to_test:
        # count the fails in a row
        consecutive_fails = consecutive_fails + 1
        
    # look for exit criteria (right click or consecutive fails)
    if consecutive_fails == max_fails:
        break
            
    # keep trial count in while loop
    trial = trial + 1
    
    # ask to continue after each trial
    ben_tools.pushToContinue(myWin)
        
# wait for keypress
# event.waitKeys()

# quit the program
core.wait(0.25)
myWin.close()
core.quit