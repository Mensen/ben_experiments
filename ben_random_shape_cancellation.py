# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 00:00:58 2016

@author: mensen
"""

from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import numpy as np
import os

# get the standard argument parser
parser = ben_tools.getStandardOptions()

# add experiment specific options
parser.add_argument("-c", "--color", dest="color_scheme", help="define color scheme", 
                  default='light')

parser.add_argument("-t", "--trial", dest="start_trial", type=int, help="difficulty to start with", 
                  default=1)                  
 
parser.add_argument("-i", "--series", dest="series", help="image series (1-4)", 
                  default='0')
                 
# get command line options
options = parser.parse_args()

# check image series
if options.series is '0':
    options.series = str(np.random.randint(1, 5))
    print ('image series %s is selected') %options.series

# randomly select obejcts (without replacement)
options.objects = np.random.choice(range(1,13), 3, replace=False)

if options.filename is not None:
    options.flag_save = True
else:
    options.filename = 'test'

# check for results directory
save_path = os.path.join('results', options.filename)
ben_tools.checkDirectory(save_path)


# main experiment
# ---------------

# get available images
image_list = []
image_path = os.path.join("rsc_images", options.color_scheme)

# sort the list alphanumerically
file_list = os.listdir(image_path)
file_list.sort()

for file in file_list:
    if options.color_scheme in file and '_' + options.series in file and file.lower().endswith(".png"):
        image_list.append(file)
  
# get object images
object_list = []
object_path = os.path.join("rsc_images", 'objects')
for file in os.listdir(object_path):
    if options.color_scheme in file and file.lower().endswith(".png"):
        object_list.append(file)
    
def objectSelect(current_image):
    
    # preallocate marker handles
    markings =  []
    marking_time = []
    position_x = []
    position_y = []
    
    # prepare the image'
    rsc_image.autoDraw=True
    rsc_image.setImage(current_image)
    rsc_image.draw(myWin)
    
    # put the image on screen
    myWin.flip()
    
    event.Mouse(visible=True)    
    # wait for a button press
    myMouse = event.Mouse(win=myWin, visible=True)
    
    # start a trial clock
    trial_clock = core.Clock()
    key_pressed = event.getKeys(timeStamped=trial_clock) 
    
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()

        # also look for keyboard presses to advance to next trial
        key_pressed = event.getKeys(keyList = ['space', 'escape'], timeStamped=trial_clock)
        
        if mouse1:
            # get the position of the click
            click_position = myMouse.getPos()
             
            # trial time
            marking_time.append(trial_clock.getTime())
             
            position_x.append(click_position[0])
            position_y.append(click_position[1])         
             
            # prepare some text
            marking_object = visual.Circle(win=myWin,
                   lineColor=(0.46, 0.76, 1),
                   lineColorSpace='rgb',
                   units='norm', 
                   pos=[click_position[0], click_position[1]],
                   radius=0.15/(n_trial + 1),
                   lineWidth=10)
            marking_object.autoDraw=True
            markings.append(marking_object)
            
            # put the marker on screen
            myWin.flip()
            core.wait(0.25)
                   
        if key_pressed:
            # if space is pressed go to next trial
            if key_pressed[0][0] == 'space':                       
                # erase markers
                for n in range(0, len(markings)):
                    markings[n].autoDraw=False
    
                # clear the screen
                rsc_image.autoDraw=False
                myWin.flip()
                
                return position_x, position_y, marking_time
            
            # TODO: if escape is pressed exit the experiment immediately
            if key_pressed[0][0] == 'escape':                       
                # erase markers
                for n in range(0, len(markings)):
                    markings[n].autoDraw=False
    
                # clear the screen
                rsc_image.autoDraw=False
                myWin.flip()
                
                # insert quit marker into position_x
                position_x[0] = 99
                return position_x, position_y, marking_time

# prepare experiment data to save
save_name = os.path.join(save_path, 'output_rsc_' + options.filename + '_s' + options.series)
data_out = data.ExperimentHandler(name='random shape cancellation', 
      version='alpha',
      dataFileName=save_name)

# open a new window
myWin = visual.Window( 
    color=[1, 1, 1], 
    fullscr=1, 
    monitor="testMonitor", 
    units="norm")

ben_tools.welcomeMessage(myWin, 'Objektfindungs Spiel')

# prepare image types for presentation
rsc_image = visual.ImageStim(myWin,
    units='norm',
    size=[2, 2])

object_image = visual.ImageStim(myWin,
    units='norm',
    size=[2, 2])
       
# run the experiment
for n_trial in range(options.start_trial - 1, 3):
    
    print n_trial    
    
    # present object alone
    object_image.setImage(os.path.join(object_path, object_list[options.objects[n_trial] - 1]))
    object_image.draw(myWin)
    # put the image on screen
    myWin.flip()
    ben_tools.waitForClick(myWin)

    # present complete image and collect press
    position_x, position_y, marking_time = objectSelect(
        os.path.join(image_path, image_list[n_trial]))

    # check for quick exit
    if position_x:
        if position_x[0] is 99:
            break

    # save the parameters
    data_out.addData('difficulty', n_trial + 1)
    data_out.addData('image', image_list[n_trial])
    data_out.addData('object', options.objects[n_trial])
    data_out.addData('n_marked',len(position_x))
    data_out.addData('times', marking_time)
    data_out.addData('position_x', position_x)
    data_out.addData('position_y', position_y)

    # go to next trial in the loop
    data_out.nextEntry()   
    
    # take a break before next trial
    if n_trial is not 2:
        ben_tools.takeABreak(myWin, 3)  
        ben_tools.pushToContinue(myWin)
    
# wait 500ms and close the screen
ben_tools.showEnd(myWin)
ben_tools.waitForClick(myWin)

core.wait(0.25)
myWin.close()
core.quit