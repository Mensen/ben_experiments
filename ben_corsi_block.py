# -*- coding: utf-8 -*-
"""
Corsi Block Test

Inselspital Bern
Sinergia Sleep and Stroke
Neuropsychological Test Battery

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import random

def boxCoordinates(centre, size):
    box_vertices = [ \
    [centre[0] - size, centre[1] - size], \
    [centre[0] - size, centre[1] + size], \
    [centre[0] + size, centre[1] + size], \
    [centre[0] + size, centre[1] - size] ]
    
    return box_vertices

def makeBlocks(n):

    box_vertices=n*[None]    
       
    my_box = n*[None]   
       
    for block in range(0, n):
        
        # get box coordinates
        box_centre = [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)]
        box_size = 0.1
        box_vertices[block] = boxCoordinates(box_centre, box_size)           
        
        # draw a block
        my_box[block] = visual.ShapeStim(win=myWin, 
                  units='norm', 
                  lineColor=[-1, -1, -1], 
                  vertices = box_vertices[block],
                  lineColorSpace='rgb',
                  lineWidth=5)            
        
#        # check for overlap (this doesn't work but may just be bad method)  
        if block > 0:       
            print "is there overlap %s" % (my_box[block].overlaps(my_box[block-1]))               

        # set to always draw after flips
        my_box[block].setAutoDraw(True)     
                             

    # look into overlap method of the shapeStim to test
                  
  #     flip the boxes on the screen                  
    myWin.flip()

    event.waitKeys()
    
    my_box[0].lineColor = [-1, -1, 1]
    
    myWin.flip()


def corsiBlockTest(n):
    return 2
    
# open a unique window
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=0, monitor="testMonitor", units="norm")

makeBlocks(4)

# wait for keypress
event.waitKeys()

# quit the program
core.wait(0.25)
myWin.close()
core.quit