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
import numpy as np
import scipy.spatial.distance

def waitForClick():
    
    # define mouse
    myMouse = event.Mouse(win=myWin, visible=True)    
    
    while True:
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
    
        if mouse1:
            return 1
        if mouse3:
            return 255
        

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
                  fillColor = [0.5, 0.5 , 0.5],
                  fillColorSpace = 'rgb',
                  lineWidth=5)      

        # set to always draw after flips
        my_boxes[block].setAutoDraw(True)     
                                                 
    # flip the boxes on the screen                  
    myWin.flip()
    #event.waitKeys()
    core.wait(2)
    return my_boxes


def corsiBlockTest(num_to_test):

    display_time = 0.5
    
    for block in range(0, num_to_test):

        my_boxes[block].fillColor = [-1, -1, 1]
        
        myWin.flip()
        
        core.wait(display_time)
        
        my_boxes[block].fillColor = [0.5, 0.5 , 0.5]

        myWin.flip()
   
    for block in range(0, num_to_test): 
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
                
                # make sure click position is within block
                if click_position[0] > my_boxes[block].vertices[0][0] and \
                click_position[0] < my_boxes[block].vertices[2][0] and \
                click_position[1] > my_boxes[block].vertices[0][1] and \
                click_position[1] < my_boxes[block].vertices[1][1]:
                    
                    # change to green
                    my_boxes[block].fillColor = [-1, 1 , -1]
                    myWin.flip()
                    # change back to grey (flipped after next click)
                    my_boxes[block].fillColor = [0.5, 0.5 , 0.5]
                    break
                
                else:
                    # change to red
                    my_boxes[block].fillColor = [1, -1 , -1]
                    myWin.flip()
                    
                    core.wait(0.5)
                    
                    # exit with 
                    for n in range(0, len(my_boxes)):
                        my_boxes[n].setAutoDraw(False)   
        
                    myWin.flip()
                                        
                    return block  
            
            if mouse3:
                for block in range(0, len(my_boxes)):
                    my_boxes[block].setAutoDraw(False)   
        
                myWin.flip() 
                return 255      
            
    # erase blocks
    core.wait(0.5)
    for block in range(0, len(my_boxes)):
        my_boxes[block].setAutoDraw(False)   
        
    myWin.flip()
    
    print "variable block is set to %.2f" % (block)    
    
    return num_to_test

def welcomeMessage(text):
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
    core.wait(1)
    
    # welcome message
    message1 = visual.TextStim(win=myWin,
       alignHoriz='center',
       alignVert='center', 
       color=(0, 0, 0),
       colorSpace='rgb',
       units='', 
       pos=[0,0],
       text='Hit any key when ready')
       
    # put the message on the screen
    message1.draw()   
    myWin.flip()
             
    # wait for mousepress
    button = waitForClick()
     

# open a unique window
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=1, monitor="testMonitor", units="norm")

# run the welcomeMessage function
welcomeMessage('Corsi Block Test')

# maximum number of trials
trials_max = 5
# starting number of boxes
num_boxes = 7
num_to_test = 3
consecutive_fails = 0
max_fails = 3

# loop trials
trial = 0
while trial < trials_max:
       
    # check for sufficient boxes
    if num_boxes < num_to_test:
        num_boxes = num_to_test
       
    # draw the boxes on screen
    my_boxes = makeBlocks(num_boxes)   
    
    # test the participant
    flag_correct = corsiBlockTest(num_to_test)

    # print result of trial in the command line
    print('you got %d of %d correct') %(flag_correct, num_to_test) 

    if flag_correct == num_to_test:
        # if correct increase number of boxes
        num_to_test = num_to_test + 1
        # reset fails if correct
        consecutive_fails = 0
    elif flag_correct < num_to_test:
        # count the fails in a row
        consecutive_fails = consecutive_fails + 1
        
    # look for exit criteria (right click or consecutive fails)
    if flag_correct == 255:
        break
    elif consecutive_fails == max_fails:
        break
            
    # keep trial count in while loop
    trial = trial + 1
        
# wait for keypress
# event.waitKeys()

# quit the program
core.wait(0.25)
myWin.close()
core.quit