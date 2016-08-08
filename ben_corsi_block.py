# -*- coding: utf-8 -*-
"""
Corsi Block Test

Inselspital Bern
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import numpy as np
import scipy.spatial.distance

def boxCoordinates(centre, size):

    size = size / 2    
    
    box_vertices = [ \
    [centre[0] - size, centre[1] - size], \
    [centre[0] - size, centre[1] + size], \
    [centre[0] + size, centre[1] + size], \
    [centre[0] + size, centre[1] - size] ]
    
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
    event.waitKeys()
    return my_boxes


def corsiBlockTest(num_box):

    for block in range(0, len(my_boxes)):

        my_boxes[block].fillColor = [-1, -1, 1]
        
        myWin.flip()
        
        core.wait(0.5)
        
        my_boxes[block].fillColor = [0.5, 0.5 , 0.5]

        myWin.flip()
   
    for block in range(0, len(my_boxes)): 
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
                
                if abs(click_position[0] - my_boxes[block].vertices[0][0]) < 0.2 and \
                abs(click_position[1] - my_boxes[block].vertices[0][1]) < 0.2:
                    
                    # change to greeen
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
    return block + 1
    
# open a unique window
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=0, monitor="testMonitor", units="norm")

num_trials = 4
# loop trials
for trial in range(0, num_trials):
    
    # draw the boxes on screen
    my_boxes = makeBlocks(trial + 3)
    # test the participant
    flag_correct = corsiBlockTest(my_boxes)

    print('you got %d of %d correct') %(flag_correct, trial + 3) 

    # look for esc key
    if flag_correct == 255:
        break
        
# wait for keypress
event.waitKeys()

# quit the program
core.wait(0.25)
myWin.close()
core.quit