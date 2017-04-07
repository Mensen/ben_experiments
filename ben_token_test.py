# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:43:09 2017

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import numpy as np
import os

# get the standard argument parser
parser = ben_tools.getStandardOptions()

# add experiment specific options
parser.add_argument("-v", "--version", dest="version", type=int, help="version: original (1) or new (2)", 
                  default=1)

parser.add_argument("-t", "--num_trials", dest="num_trials", type=int, help="number of trials (default:10)", 
                  default=10)

# get command line options
options = parser.parse_args()

# process arguments (overwrite false flag_test if filename given)
if options.filename is not None:
    options.flag_save = True
else:
    options.filename = 'test'

# check for results directory
save_path = os.path.join('results', options.filename)
ben_tools.checkDirectory(save_path)


# define color_scheme
def defineColors():

    color_scheme = np.ones((4, 5, 3))
    
    COLOR_BLUE = np.array([-1, -1, 1])
    COLOR_RED = np.array([1, -1, -1])
    COLOR_YELLOW = np.array([1, 1, -1])
    COLOR_GREEN = np.array([-1, 0.75, -1])
    
    # all the blues
    color_scheme[0,0] = COLOR_BLUE
    color_scheme[1,1] = COLOR_BLUE
    color_scheme[2,4] = COLOR_BLUE
    color_scheme[3,3] = COLOR_BLUE
    # all the reds
    color_scheme[0,1] = COLOR_RED
    color_scheme[1,2] = COLOR_RED
    color_scheme[2,3] = COLOR_RED
    color_scheme[3,0] = COLOR_RED 
    # all the yellow
    color_scheme[0,3] = COLOR_YELLOW 
    color_scheme[1,0] = COLOR_YELLOW
    color_scheme[2,1] = COLOR_YELLOW
    color_scheme[3,4] = COLOR_YELLOW
    # all the greens
    color_scheme[0,4] = COLOR_GREEN
    color_scheme[1,3] = COLOR_GREEN
    color_scheme[2,2] = COLOR_GREEN
    color_scheme[3,1] = COLOR_GREEN
    
    return color_scheme

# draw the shapes on screen
def drawTokens():

    objects = [[0] * 5 for n in range(4)]
   
    # draw circles
    for row in range(0, 2):
        for shape in range(0, 5):
        
            objects[row][shape] = visual.Circle(win=myWin,
               lineColor=background_color, 
               fillColor=color_scheme[row, shape],
               units='pix', 
               pos=[object_x_centers[shape], object_y_centers[row]],
               radius=70 / np.sqrt(row+1),
               lineWidth=10)
                       
            objects[row][shape].setAutoDraw(True)
    
    # draw rectangles
    for row in range(2, 4):
        for shape in range(0, 5):
        
            # TODO: don't just guestimate the sizes
            objects[row][shape] = visual.Rect(win=myWin,
               lineColor=background_color, 
               fillColor=color_scheme[row, shape],
               units='pix', 
               pos=[object_x_centers[shape], object_y_centers[row]],
               width=60 / (row) * 4,
               height=80 / (row) * 4,
               lineWidth=10)
                       
            objects[row][shape].setAutoDraw(True)
    
    myWin.flip()
    core.wait(0.1)
    
    return objects
     
def runTrial():
    
    # pre-allocate answers so we can append to them for double answers
        
    
    # present the task question using audio file

    # start a trial clock
    trial_clock = core.Clock()    
    
    # wait for a button press
    myMouse = event.Mouse(win=myWin, visible=True)
    
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
           
        if mouse1:
            # get the position of the click
            myMouse.clickReset()
            click_position = myMouse.getPos()
                
#            print('click position is %d %d') %(click_position[0], click_position[1])
            # get trial time
            trial_time = trial_clock.getTime() 

            # figure out which line was clicked on
            distance_to_shapes = object_x_centers - click_position[0]
            shape_index = (np.abs(distance_to_shapes)).argmin()

            distance_to_rows = object_y_centers - click_position[1]
            row_index = (np.abs(distance_to_rows)).argmin()
            
#            print('distance to shape is %d %d') %(distance_to_shapes[shape_index], distance_to_rows[row_index])            
                        
            if abs(distance_to_shapes[shape_index]) < 80 and \
            abs(distance_to_rows[row_index]) < 80:
              
                objects[row_index][shape_index].lineColor = [-1, -1, -1]
                myWin.flip()
                core.wait(1)            

                # return to normal
                objects[row_index][shape_index].lineColor = background_color
                myWin.flip()
                break
            
            else:
                
                # replay the trial instruction
                x = 1                
                
        if mouse3:
            
            row_index = 100
            shape_index = 100
            trial_time = 0
            break

    return row_index, shape_index, trial_time
      
    
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section
# prepare experiment data to save
save_name = os.path.join(save_path, 'output_tt_' + options.filename)
data_out = data.ExperimentHandler(name='token test', 
    version=options.version, 
    dataFileName=save_name)   

# open a unique window
background_color = ((np.array([58, 61, 59])/255.0) - 0.5) * 2
highlight_color = ((np.array([248, 248, 255])/255.0) - 0.5) * 2

myWin = visual.Window([1000, 800], color=background_color, fullscr=1, monitor="testMonitor", units="pix")

print('screen size is %d') %(myWin.size[0]) 

# run the welcomeMessage function
# ben_tools.welcomeMessage(myWin, 'Token Test')

# TODO: actually get screen size and adjust
object_x_centers = np.linspace(-500, 500, num = 5)
object_y_centers = np.linspace(-300, 300, num = 4)

# loop trials
color_scheme = defineColors()
objects = drawTokens()

for n in range(0, options.num_trials):
    
    # run the trial
    row_index, shape_index, trial_time = runTrial();
    
    # check if quit
    if row_index is 100:
        break
    
    # check if correct
    
    # record the results
    data_out.addData('question', n + 1)
    data_out.addData('row', row_index + 1)
    data_out.addData('shape', shape_index + 1)
    data_out.addData('time', trial_time)
    data_out.addData('correct', 0)
    
    data_out.nextEntry()    


# print result of trial in the command line
print('you hit row %d and shape %d') %(row_index + 1, shape_index + 1) 

# quit the program
core.wait(0.25)
myWin.close()
core.quit                   