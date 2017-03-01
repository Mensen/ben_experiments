# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 19:16:37 2017

@author: mensen
"""

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
    
# open new window
myWin = visual.Window( 
    color=[1, 1, 1], 
    fullscr=1, 
    monitor="testMonitor", 
    units="norm")

# run the welcomeMessage function
ben_tools.welcomeMessage(myWin, 'Wortfindungstest')
    
# pre-allocate trial time
num_trials = len(image_list) - 1
trial_time = num_trials * [0]
trial_response = num_trials * [0]

# loop each trial
for n_trial in range(0, num_trials):

    # start with fixation cross
    

    # prepare the image
    bwt_image = visual.ImageStim(myWin,
    pos=[0,0],                             
    units='norm',
    size=[1, 2])

    # set the specific image
    bwt_image.setImage(os.path.join(image_path, image_list[n_trial]) + '.jpg')
    bwt_image.draw(myWin)
    # put the image on screen
    myWin.flip()
    
    # start a trial clock
    trial_clock = core.Clock()          
    
    # wait for mouse click
    myMouse = event.Mouse(win=myWin, visible=True)
    
    # eliminate previous recording
    frames = []    
    
    while True:
        
        myMouse.clickReset()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        
        # collect the audio data
        data = stream.read(CHUNK)
        frames.append(data)        
        
        if mouse1:
            trial_response[n_trial] = 1
            break
            
        elif mouse3:
            trial_response[n_trial] = 0
            break
    
    # record trial time
    trial_time[n_trial] = trial_clock.getTime()            

    # save audio recording      
    wf = wave.open(os.path.join(save_path, 'audio', 'bwt_' + options.filename + '_' + image_list[n_trial]), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # save the parameters
    data_out.addData('object_name', image_list[n_trial])
    data_out.addData('response', trial_response[n_trial])
    data_out.addData('time', trial_time[n_trial])
    
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