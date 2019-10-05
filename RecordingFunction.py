from GlobalVariables import *
import pyaudio, wave

def audio_record(j,WAVE_OUTPUT_FILENAME,RECORD_SECONDS,progress_bar):
    '''
    The function to record the audio from mic.

    Parameters:
        j : The iterable count to know the count of recorded file.
        WAVE_OUTPUT_FILENAME : The audio file path where recorded audio will be saved.
        RECORD_SECONDS : Number of seconds for which audio will be recorded.
        progress_bar : The variable to update progress_bar widget is it is present, else 'NULL' is passed.
    '''

    frames = []
    # Creating pyaudio object and set the required parametrs.
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("*********** recording:"+str(j)+' ***********')
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # Start the recording.
        data = stream.read(CHUNK)
        frames.append(data)
        if progress_bar!='NULL':
            # Progress bar to increase per step.
            progress_bar.step(1)
    print("*********** done recording:"+str(j)+' ***********')
    # Closing the audio recording stream.
    stream.stop_stream()
    stream.close()
    p.terminate()
    # Save the audio file.
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
