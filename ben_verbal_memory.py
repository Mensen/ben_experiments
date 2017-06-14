# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:00:25 2017

@author: sinergia
"""
from psychopy import visual, core, event, data  # import some libraries from PsychoPy
import ben_tools
import os
import random
import pyaudio  
import wave

# import the word list    
word_file = open(os.path.join('vmt_stimuli', 'vmt_word_list.txt'), 'r')    
word_list = word_file.read().split('\n')

# randomise the list
randomised_list = random.sample(word_list, len(word_list))

START_NUMBER = 2
TRIALS_MAX = 3

def playAudio(current_word):
    # open the audio file (n + 1 because of 0 indexing)
    f = wave.open("vmt_stimuli/" + current_word + ".wav", "rb")  

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

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# main section
    
#instantiate PyAudio  
p = pyaudio.PyAudio()
#define stream chunk   
CHUNK_SIZE = 1024

num_to_test = START_NUMBER
trial = 0
n_played = 0

# run the trials
while trial < TRIALS_MAX:
    
    current_wordlist = randomised_list[n_played : n_played + num_to_test]
    
    for n in range(0, num_to_test):
        # play each word
        playAudio(current_wordlist[n])
        core.wait(0.5)
    
    # count already played
    n_played += num_to_test     
    
    # count trials
    num_to_test += 1
    trial += 1
    