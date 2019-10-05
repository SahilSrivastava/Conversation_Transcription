from GlobalVariables import *
from datetime import datetime
from pydub import AudioSegment
import tkinter as tk
import pyaudio, contextlib, wave, os, pickle
import azure.cognitiveservices.speech as speechsdk

class Value:
    COUNT = 0
    API_RATE = 0

class ChunkDataList:
    '''A class to keep record of each audio's speaker, transcription and confidence.'''

    def __init__(self,count,speaker,speech_to_text,confidence):
        self.count = count
        self.speaker = speaker
        self.speech_to_text = speech_to_text
        self.confidence = confidence

def get_duration(fname):
    '''
    The fuction to get the duration of audio.

    Parameters:
        frame : The audio file received to find the duration.

    Return:
        duration : The duration of audio.
    '''

    # A function to get the duration of the audio.
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def audio_segments(j,total_duration,WAVE_OUTPUT_FILENAME,type_e):
    '''
    The fuction to segment the audio.

    Parameters:
        j : The iterable variable which tells the audio file number. It is zero while adding profile.
        total_duration : It contain the duration of receiving audio file.
        WAVE_OUTPUT_FILENAME : The path to the audio file.
        type_e : Parameter to tell whether transcription is live or not.
    '''

    # Audio segmentation into three parts. The audio segmentation can be improved by using pyAudioAnalysis library which helps in segmenting the audio based on silence.
    n = 3
    chunk_time = total_duration / n
    t1 = 0 * 1000
    t2 = chunk_time * 1000
    for i in range(n):
        # Loading the file.
        newAudio = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
        newAudio = newAudio[t1:t2]
        # Change the segment folder based on parameter.
        if type_e == "live":
            newAudio.export('Samples\Live_Segments\Output_'+str(j)+"\\" + str(i) + ".wav", format="wav")
        elif type_e == "import":
            newAudio.export('Samples\Import_chunks\\' + str(i) + ".wav", format="wav")
        else:
            print("ERROR")
            return
        t1 = t2
        t2 = t2 + (chunk_time * 1000)

def logData(count,speaker,speech,confidence):
    '''
    The function to dump the transcription into a txt file.

    Parameters:
        count : An iterable variable needed to record transcripted audio number.
        speaker : The name of audio file's speaker.
        speech : The transcription of audio file.
        confidence : The measure to know how much accurate is predicted speaker.

    Return:
        line : A string containing count,speaker,confidence and transcription.
    '''

    # A function to dump the transcription into txt file.
    with open("Dump.txt",'a') as dp:
        line = str(count) + " " + speaker +" ("+confidence+") "+ ": " + speech
        print(line)
        dp.writelines(line)
        dp.write("\n")
        return line

def speech_recognize_once_from_file(file):
    '''
    The function to get the transcription of audio file.

    Parameter:
        file : The audio file needed to be transcribed.

    Return :
        result.text : The transcribed speech
    '''

    #Function to get the transcription.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename = file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return result.no_match_details
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def update_list(list_text,type_e):
    '''
    The function to update the listview and textview.

    Parameter:
        list_text : The tkinter list widget need to be updated.
        type_e : Tells whether the tkinter widget is listview or textview.
    '''

    # Function to update the list whenever there is any change.
    try:
        pickle_in = open("my_dict.pickle","rb")
        in_dict = pickle.load(pickle_in)
        pickle_in.close()
        if type_e=="list":
            list_text.delete('0','end')
            for value in in_dict.values():
                list_text.insert('end',value)
        elif type_e=="text":
            list_text.config(state= "normal")
            list_text.delete(1.0,'end')
            for value in in_dict.values():
                list_text.insert('end',value+"\n")
            list_text.config(state= "disable")
        else:
            print("Wrong Input in 'update_list' function.\nOnly 'text' or 'list' is allowed as second argument.")
            pass
    except :
        pass
