# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:43:09 2017

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
parser.add_argument("-v", "--version", dest="version", type=int, help="version: original (1) or new (2)", 
                  default=1)

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


# define rectangle coordinates
def boxCoordinates(centre, size):

    screen_ratio = 14/9.0

    size = size / 2
    
    box_vertices = [ \
    [centre[0] - size / screen_ratio, centre[1] - size], \
    [centre[0] - size / screen_ratio, centre[1] + size], \
    [centre[0] + size / screen_ratio, centre[1] + size], \
    [centre[0] + size / screen_ratio, centre[1] - size] ]
    
    return box_vertices

# draw the shapes on screen
def drawTokens():

    object_x_centers = np.linspace(-1, 1, num = 7)
    object_y_centers = np.linspace(-1, 1, num = 6)
    
    # draw circles
    for row in range(0, 2):
        for shape in range(1, 6):
        
            object[row, shape] = visual.Circle(win=myWin,
               lineColor=(0.46, 0.76, 1),
               lineColorSpace='rgb',
               units='norm', 
               pos=[object_x_centers[object_x_centers[row]], object_y_centers[shape]],
               radius=0.15,
               lineWidth=10)
                       
                       
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section
# prepare experiment data to save
save_name = os.path.join(save_path, 'output_tt_' + options.filename)
data_out = data.ExperimentHandler(name='token test', 
    version=options.version, 
    dataFileName=save_name)   

# open a unique window
myWin = visual.Window([1000, 800], color=[1, 1, 1], fullscr=1, monitor="testMonitor", units="norm")

# run the welcomeMessage function
ben_tools.welcomeMessage(myWin, 'Corsi Block Test')

# loop trials
drawTokens()

button = waitForClick(myWin)

# quit the program
core.wait(0.25)
myWin.close()
core.quit                   