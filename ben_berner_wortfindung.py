# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 19:16:37 2017

@author: mensen
"""
from __future__ import division
from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import os
import csv
import pyaudio
import wave

# define audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# define fixed variables
MAX_TIME = 10

# get the standard argument parser
parser = ben_tools.getStandardOptions()

# add experiment specific options
parser.add_argument("-l", "--list", dest="image_list", help="list of images to present", 
                  default='bwt_example_list.txt')
                                  
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
ben_tools.checkDirectory(os.path.join(save_path, 'audio'))

# where are the images located
image_path = 'bwt_images'

# read participant list
with open(options.image_list, 'rb') as f:
    reader = csv.reader(f, delimiter=' ')
    image_list = list(reader)
    image_list = image_list[0]

# prepare the audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
    input=True, output=True,
    frames_per_buffer=CHUNK)
        
# initialise experiment
# prepare experiment data to save
data_out = data.ExperimentHandler(name='object recognition', 
      version='alpha', 
      dataFileName=os.path.join(save_path, 'output_bwt_' + options.filename),
      savePickle=options.flag_save,
      saveWideText=options.flag_save)

def showFixation():
    
    # draw fixation cross
    cross_object = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center',
           units='norm',
           height=0.6,           
           color=(0, 0, 0),
           colorSpace='rgb',
           pos=[0,0],
           text='+')
           
    # put the image on screen
    cross_object.draw()
    myWin.flip()    

def showEnd():
    
    # draw end text
    cross_object = visual.TextStim(win=myWin,
           alignHoriz='center',
           alignVert='center',
           units='norm',
           height=0.6,           
           color=(0, 0, 0),
           colorSpace='rgb',
           pos=[0,0],
           text='Danke!')
           
    # put the image on screen
    cross_object.draw()
    myWin.flip() 

def runTrial(): 
    
    # prepare the image
    bwt_image = visual.ImageStim(myWin,
    pos=[0,0],                             
    units='pix')
       
    # set the specific image
    bwt_image.setImage(os.path.join(image_path, image_list[n_trial]) + '.jpg')

    # find the image size  
    image_size = bwt_image.size
    image_ratio = image_size[0] / image_size[1]

#    print('image size was %d by %d, window ratio is %f, image ratio %f') %(image_size[0], image_size[1], window_ratio, image_ratio)

    # adjust the image size to screen
    if image_ratio > window_ratio:
        # longer picture
        adjust_value = window_size[0] / image_size[0]
    else:
        # taller picture
        adjust_value = window_size[1] / image_size[1]

    bwt_image.size = [image_size[0] * adjust_value, image_size[1] * adjust_value]
#    print('image size is %d by %d, adjust factor %f') %(bwt_image.size[0], bwt_image.size[1], adjust_value)
    
    bwt_image.draw(myWin)
    # put the image on screen
    myWin.flip()
    
    # start a trial clock
    trial_clock = core.Clock()          
    
    # wait for mouse click
    myMouse = event.Mouse(win=myWin, visible=True)
    
    # eliminate previous recording
    frames = []
    
    # reset variables
    response_time = MAX_TIME
    flag_stop = False
    
    while trial_clock.getTime() < MAX_TIME:
    
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        
        # collect the audio data
        data = stream.read(CHUNK)
        frames.append(data)        
        
        if mouse1:
            response_time = trial_clock.getTime()
            
            if n_trial is not num_trials - 1:
                showFixation()
                flag_stop = True
            else:
                showEnd()
                flag_stop = True
        
        elif mouse3:
            response_time = 0
            break
        
        if flag_stop:
            if trial_clock.getTime() > response_time + 1.5:
                break
          
    
    # save audio recording      
    wf = wave.open(os.path.join(save_path, 'audio', 'bwt_' + options.filename + '_' + image_list[n_trial] + '.wav'), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    if response_time >= MAX_TIME:
        showFixation()
        core.wait(1.5)
    
    return response_time
    

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section

# open new window
myWin = visual.Window( 
    color=[1, 1, 1], 
    fullscr=1, 
    monitor="testMonitor", 
    units="pix")

window_size = myWin.size
window_ratio = window_size[0]/window_size[1]
print('screen size is %d') %(window_size[0]) 

# run the welcomeMessage function
ben_tools.welcomeMessage(myWin, 'Wortfindungstest')
    
# pre-allocate trial time
num_trials = len(image_list) - 1
trial_time = num_trials * [0]
trial_response = num_trials * [0]

# fixation window to start
showFixation()
core.wait(2)

# loop each trial
for n_trial in range(0, num_trials):

    response_time = runTrial()

    # check for stopping condition
    if response_time is 0:
        break

    # save the parameters
    data_out.addData('object_name', image_list[n_trial])
    data_out.addData('time', response_time)
    
    # go to next trial in the loop
    core.wait(0.25)
    data_out.nextEntry()

# cleanup audio 
stream.stop_stream()
stream.close()
p.terminate()

# wait after final trial then exit
core.wait(0.5)

myWin.close()
core.quit