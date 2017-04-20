# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:43:09 2017

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import numpy as np
import os
import pyaudio  
import wave

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

# maximum of 10 trials
if options.num_trials > 10:
    options.num_trials = 10

# check for results directory
save_path = os.path.join('results', options.filename)
ben_tools.checkDirectory(save_path)

# manually define number of expected answers to each question
n_answers = [1, 1, 2, 2, 1, 1, 1, 2, 2, 2]


# define color_scheme
def defineColors(version):
   
    COLOR_BLUE = np.array([-1, -1, 1])
    COLOR_RED = np.array([1, -1, -1])
    COLOR_YELLOW = np.array([1, 1, -1])
    COLOR_GREEN = np.array([-1, 0.75, -1])
    
    if version is 1:
        # pre-allocate color_scheme
        color_scheme = np.ones((2, 5, 3))

        # in row order
        color_scheme[0, 0] = COLOR_YELLOW
        color_scheme[0, 1] = COLOR_RED
        color_scheme[0, 2] = COLOR_BLUE
        color_scheme[0, 3] = COLOR_GREEN        
        
        color_scheme[1, 0] = COLOR_GREEN
        color_scheme[1, 1] = COLOR_YELLOW
        color_scheme[1, 3] = COLOR_BLUE
        color_scheme[1, 4] = COLOR_RED
               
    elif version is 2:
        # pre-allocate color_scheme
        color_scheme = np.ones((4, 5, 3))
        
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
def drawTokens(version):

    row_range = [0]*2

    if version is 1:
        objects = [[0] * 5 for n in range(2)]
        row_range[0] = range(0, 1)
        row_range[1] = range(1, 2)
        
        circle_radius = 80
        rectangle_height = 200

    elif version is 2:
        objects = [[0] * 5 for n in range(4)]
        row_range[0] = range(0, 2)
        row_range[1] = range(2, 4)
        
        circle_radius = 70
        rectangle_height = 180


    # draw circles
    row_counter = 0
    for row in row_range[0]:
        
        row_counter += 1        
        
        for shape in range(0, 5):
        
            objects[row][shape] = visual.Circle(win=myWin,
               lineColor=background_color, 
               fillColor=color_scheme[row, shape],
               units='pix', 
               pos=[object_x_centers[shape], object_y_centers[version-1][row]],
               radius= circle_radius / np.sqrt(row_counter),
               lineWidth=10)
                       
            objects[row][shape].setAutoDraw(True)
    
    # draw rectangles
    row_counter = 0
    for row in row_range[1]:

        row_counter += 1        
        
        for shape in range(0, 5):
        
            # TODO: don't just guestimate the sizes
            objects[row][shape] = visual.Rect(win=myWin,
               lineColor=background_color, 
               fillColor=color_scheme[row, shape],
               units='pix', 
               pos=[object_x_centers[shape], object_y_centers[version-1][row]],
               width= (rectangle_height * 0.75) / np.sqrt(row_counter),
               height= rectangle_height / np.sqrt(row_counter),
               lineWidth=10)
                       
            objects[row][shape].setAutoDraw(True)
    
    myWin.flip()
    core.wait(0.1)
    
    return objects

def eraseTokens():
    
    for row in range(0, len(objects)):
        for shape in range(0, 5):
            
            objects[row][shape].setAutoDraw(False)

def playAudio():
    # open the audio file (n + 1 because of 0 indexing)
    f = wave.open("token_test_audio/tt_" + str(n + 1) + ".wav","rb")  

    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(CHUNK_SIZE)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(CHUNK_SIZE)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  

def runTrial(expected_answers):
    
    # pre-allocate answers so we can append to them for double answers
    row_selected = []
    shape_selected = []
    trial_time = []    
    
    # present the task question using audio file
    playAudio()

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
            temp_time = trial_clock.getTime() 

            # figure out which line was clicked on
            distance_to_shapes = object_x_centers - click_position[0]
            shape_index = (np.abs(distance_to_shapes)).argmin()

            distance_to_rows = object_y_centers[version-1] - click_position[1]
            row_index = (np.abs(distance_to_rows)).argmin()
            
#            print('distance to shape is %d %d') %(distance_to_shapes[shape_index], distance_to_rows[row_index])            
#            print('shape_index is %d, row index is %d') %(shape_index, row_index)            
                        
                        
            if abs(distance_to_shapes[shape_index]) < 80 and \
            abs(distance_to_rows[row_index]) < 80:
              
                objects[row_index][shape_index].lineColor = [-1, -1, -1]
                myWin.flip()
                core.wait(1)            

                # return to normal
                objects[row_index][shape_index].lineColor = background_color
                myWin.flip()
                
                # store the result
                row_selected.append(row_index + 1)
                shape_selected.append(shape_index + 1)   
                trial_time.append(temp_time)
                           
            else:
                
                # replay the trial instruction
                playAudio()
                
        if mouse3:
            
            # overwrite any previous answer and exit
            row_selected = 100
            shape_selected = 100
            trial_time = 0
            break

        # check for sufficient responses (1 or 2)
        if len(row_selected) is expected_answers:
            break
        
    return row_selected, shape_selected, trial_time
      
    
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section
    
#instantiate PyAudio  
p = pyaudio.PyAudio()     
#define stream chunk   
CHUNK_SIZE = 1024
    
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
ben_tools.welcomeMessage(myWin, 'Token Test')

# TODO: actually get screen size and adjust
object_x_centers = np.linspace(-500, 500, num = 5)

# Y centers change depending on question number
object_y_centers = [0]*2
object_y_centers[0] = np.linspace(-200, 200, num = 2)
object_y_centers[1] = np.linspace(-300, 300, num = 4)

# get the colorscheme and then draw the token
version = 1
color_scheme = defineColors(version)
objects = drawTokens(version)

# loop trials
for n in range(0, options.num_trials):
    
    # run the trial
    row_index, shape_index, trial_time = runTrial(n_answers[n]);
    
    # check if quit
    if row_index is 100:
        break
    
    # TODO: check if correct
    
    # record the results
    data_out.addData('question', n + 1)
    data_out.addData('row', row_index)
    data_out.addData('shape', shape_index)
    data_out.addData('time', trial_time)
    data_out.addData('correct', 0)
    
    data_out.nextEntry()    

    # switch tokens after n = 3
    if n is 3:
        eraseTokens()
        version = 2
        color_scheme = defineColors(version)
        objects = drawTokens(version)

# print result of trial in the command line
print('you hit row %d and shape %d') %(row_index + 1, shape_index + 1) 

# quit the program
eraseTokens()
ben_tools.showEnd(myWin)
ben_tools.waitForClick(myWin)

core.wait(0.25)
myWin.close()
core.quit                   