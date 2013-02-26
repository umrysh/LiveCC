#Based On  python-google-speech-scripts [https://github.com/jeysonmc/python-google-speech-scripts]
import pyaudio
import wave
import audioop
from collections import deque 
import os
import urllib2
import urllib
import time
from microsofttranslator import Translator

#Set Debug flag
DEBUG=False

def debug_print(text):
    if(DEBUG):
        print text

def listen_for_speech():
    """
    Does speech recognition using Google's speech  recognition service.
    Records sound from microphone until silence is found and save it as WAV and then converts it to FLAC. Finally, the file is sent to Google and the result is returned.
    """
    #open stream
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)

    debug_print("* listening. CTRL+C to finish.")
    all_m = []
    data = ''
    rel = RATE/chunk
    slid_win = deque(maxlen=SILENCE_LIMIT*rel)
    started = False
    
    try:
        while (True):
            data = stream.read(chunk)
            slid_win.append (abs(audioop.avg(data, 2)))

            if(True in [ x>THRESHOLD for x in slid_win]):
                if(not started):
                    debug_print("starting record")
                started = True
                all_m.append(data)
            elif (started==True):
                debug_print("finished")
                print("***")
                #the limit was reached, finish capture and deliver
                filename = save_speech(all_m,p)
                stt_google_wav(filename)
                #reset all
                started = False
                slid_win = deque(maxlen=SILENCE_LIMIT*rel)
                all_m= []
                debug_print("listening ...")
    except KeyboardInterrupt:
        debug_print("\nuser stopped the recording")
        if (started==True):
            filename = save_speech(all_m,p)
            stt_google_wav(filename)

    debug_print("* done recording")
    stream.close()
    p.terminate()


def save_speech(data, p):
    filename = 'output_'+str(int(time.time()))
    # write data to WAVE file
    data = ''.join(data)
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()
    return filename


def stt_google_wav(filename):
    #Convert to flac
    os.system(FLAC_CONV+ filename+'.wav > /dev/null 2>&1') # Linux
    #os.system(FLAC_CONV+ filename+'.wav > nul 2>&1') # Windows

    f = open(filename+'.flac','rb')
    flac_cont = f.read()
    f.close()

    #post it
    lang_code='en-US'
    googl_speech_url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6'%(lang_code)
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",'Content-type': 'audio/x-flac; rate=16000'}
    req = urllib2.Request(googl_speech_url, data=flac_cont, headers=hrs)
    p = urllib2.urlopen(req)

    try:
        res = eval(p.read())['hypotheses'][0]['utterance']
        debug_print(res)
        temp = translator.translate(res, SPANISH)
        print (res + " <> " + temp.encode('utf-8'))
        map(os.remove, (filename+'.flac', filename+'.wav'))
        return res
    except:
        debug_print("no data")
        map(os.remove, (filename+'.flac', filename+'.wav'))
        return "no data"
    

FLAC_CONV = 'flac -f ' # We need a WAV to FLAC converter.
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

#Globals for translation
SPANISH = "es"
translator = Translator('<Your Client ID>', '<Your Client Secret>')

if(__name__ == '__main__'):
    global THRESHOLD #The threshold intensity that defines silence signal (lower than).
    global SILENCE_LIMIT #Silence limit in seconds. The max ammount of seconds where only silence is recorded. When this time passes the recording finishes and the file is delivered.

    answer = raw_input("Enter Your Threshold (Default=380): ")
    if(answer):
        THRESHOLD = int(answer)
    else:
        THRESHOLD = 380

    print "Threshold Set at %s\n" % THRESHOLD

    answer = raw_input("Enter Your Silence Limit (Default=2): ")
    if(answer):
        SILENCE_LIMIT = int(answer)
    else:
        SILENCE_LIMIT = 2 

    print "Silence Limit Set at %s\n" % SILENCE_LIMIT

    listen_for_speech()
