import os
from re import A
from flask import Flask, json, request
import uuid

import flask
import time

from scipy.io import wavfile
from pydub import AudioSegment


import numpy as np
from scipy.fft import fft
import statistics


app = Flask(__name__)



f1=100
f2=1000

margin=1 # margin filter, 1s

approaching=2 #0 false, 1 true, 2 null
start_max = []
start_A_vect = [0]
second = 0
resume = False

b=0



def getThreshold():
    global start_max
    global start_A_vect
    global second
    global resume

    threshold:int

    if len(start_max)>=60:
        start_max.pop(0)
    if len(start_A_vect)>=60:
        start_A_vect.pop(0)
 
    if second==1: # and not resume:
        second=3
        start_A_vect.append(max(start_max))
        start_A_vect.append(max(start_max))
        start_A_vect.append(max(start_max))
        threshold = start_A_vect[-1]
    elif second>=10: # or resume:
        sA=start_max[-10:]
        start_A_vect.append(np.percentile(sA,70))
        mA=statistics.median(start_A_vect)

        #THRESHOLD CONTROL
        if start_A_vect[-1]<mA: 
            threshold=mA
        else:
            if start_A_vect[-1]>2*mA:
                threshold=2*mA
            else:
                threshold= start_A_vect[-1]
        
        

    else:
        start_A_vect.append(start_A_vect[-1])
        threshold = start_A_vect[-1]
    

    return threshold


def getFilter(data, A):
    global approaching
    global margin
    global b

    H=False
    if data>A:
        if approaching==1:
            b=0
            H=True
        elif approaching==2:
            H=True
            approaching=1
            b=0
        else:
            approaching=0
    elif b<margin and approaching==1:
        H=True
        b+=1
    else:
        approaching=2

    return H


def getWarning(data):
    global second
    second+=1

    data_fft = fft(data)
    data_abs = abs(data_fft)

    f_vehicle = data_abs[f1:f2]
    max_f = max(f_vehicle)

    #THRESHOLD
    start_max.append(max_f)
        
    return getFilter(max_f, getThreshold())
    


###############################################################################################################

def stop():
    global approaching
    global start_max 
    global start_A_vect 
    global second 
    global resume 
    global b


    time.sleep(0.25)
    b=0
    approaching=2 #0 false, 1 true, 2 null
    start_max = []
    start_A_vect = [0]
    second = 0
    resume = False


def pause():
    global approaching
    global second
    global resume 
    global b

    time.sleep(0.25)
    b=0
    approaching=2 #0 false, 1 true, 2 null
    second = 0
    resume = True


###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################


@app.route('/status/<status>', methods=['POST'])

def upload_file(status):
    global second


    if status=='play':
        #POST
        
        file = request.files['AudioFile']

        if not file.filename.endswith('.wav'):
            return 'File extension must be .wav', 415  # Unsupported Media Type
        
        path = './temp.wav'
        file.save(path)
        file.flush()
        file.close() 
        
        src = path
        dst = "./audio.wav"

        # convert wav to mp3                                                            
        sound = AudioSegment.from_file(src)
        sound.export(dst, format="wav")

        #os.remove(src)

        fs,audio=wavfile.read('./audio.wav')
        
        warning = getWarning(audio)

        response = flask.jsonify({'warning': warning})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    elif status=='pause':
        pause()
        response = flask.jsonify({'connection': 'pause'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    elif status=='stop':
        stop()
        response = flask.jsonify({'connection': 'stop'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    


if __name__ == '__main__':
    app.run('193.170.63.37', 8080, debug=True)