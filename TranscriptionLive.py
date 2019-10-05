from datetime import datetime
from tkinter import messagebox
from AllApiFiles import *
from UtilFunctions import *
from RecordingFunction import *
import tkinter as tk
import urllib.request as url
import wave, threading, os, time, glob, contextlib, pickle, shutil, urllib


instance = Value()
class Identify(tk.Frame):
    '''The class to do audio transcription by live recording the audiofiles.'''

    stop_thread_t1 = True
    stop_thread_t2 = True
    j=0
    CHUNK_DATA_OBJECTS = []
    profile_info = {}
    rec_start = 0

    def __init__(self, parent, controller):
        '''
        The constructor of ImportIdentify class that define basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        def record():
            '''The function the fuction to record and call the fuction to segment the audio file.'''

            textLabel_1.configure(text="\n Started Recording")
            display.config(state='normal')
            display.delete(1.0,'end')
            display.config(state='disable')
            start_btn.config(state="disable")
            stop_rec_btn.config(state="normal")
            backButton.config(state='disable')
            self.j = 0
            instance.COUNT = 0
            self.rec_start = 1
            # Getting the current datetime to create a new folder
            cwd = os.getcwd()
            today_folder = datetime.now()
            today_folder = today_folder.strftime("%d-%m-%Y_%H-%M-%S")
            os.mkdir(cwd + "\\Recordings\\"+today_folder)
            while self.stop_thread_t1:
                WAVE_OUTPUT_FILENAME = cwd + "\\Recordings\\"+today_folder+"\\Output_"+str(self.j) + ".wav"
                # Record the audio, the process will be continuous.
                audio_record(self.j,WAVE_OUTPUT_FILENAME,10,'NULL')
                try:
                    os.mkdir("Samples\Live_Segments\Output_"+str(self.j))
                except FileExistsError:
                    print("Folder Already exists:","Samples\Live_Segments\Output_"+str(self.j))
                # Segment the audio into small audio files.
                audio_segments(self.j,10,WAVE_OUTPUT_FILENAME,"live")
                self.j=self.j+1
            textLabel_1.configure(text="\n Recording Done")
            textLabel_2.configure(text="Wait for Transcription to Complete")
            stop_rec_btn.config(state="disable")
            stop_trans_btn.config(state="normal")

        def identify(list_chunk):
            '''
            The function to recieve a chuck of audio list and process each of the audio file and tell it's transcription, speaker and confidence.

            Parameters:
                list_chunk : The list of segmented audiofiles recieved from 10 second audio files.
            '''

            print("Starting Process")
            speech_data = ''
            speaker_data = ''
            # Loading of the id of profiles from pickle file and used for transcription
            pickle_in = open("profile_selected.pickle","rb")
            profile_id_list_all = pickle.load(pickle_in)
            pickle_in.close()
            try:
                profile_id_list = [keys for keys in profile_id_list_all.keys()]
            except Exception as e:
                print("Error in getting profile Ids",str(e))
            for each_chunk in list_chunk:
                # If the chunk is less than one second, then reject it.
                if get_duration(each_chunk) > 1.0:
                    instance.API_RATE += 1
                    if(instance.API_RATE < 10):
                        instance.COUNT += 1
                        try:
                            #get the transcription of the audio.
                            speech_data = speech_recognize_once_from_file(each_chunk)
                        except Exception as e:
                            print("Exception in speech to text",str(e))
                            print("Skipping chunk: {}".format(each_chunk))
                            continue
                        try:
                            print("identifying Speaker")
                            # Get the profile and confidence.
                            speaker_object = identify_file(OCM_API,each_chunk,"True",profile_id_list)
                            speaker_data = speaker_object.get_identified_profile_id()
                            confidence = speaker_object.get_confidence()
                        except Exception as e:
                            print("Exception in speaker",str(e),)
                            print("Speaker for wav{} has set to Blank".format(each_chunk))
                            speaker = "NULL"
                            continue
                        self.CHUNK_DATA_OBJECTS.append(ChunkDataList(instance.COUNT,speaker_data,speech_data,confidence))
                    else:
                        instance.API_RATE = 0
                        time.sleep(10)
                else:
                    print("Skipping Chunk" , each_chunk, get_duration(each_chunk))
                    continue

        def transcription():
            '''
            The function to fetch the segmented audio files from a folder and send to 'identity' function as audio list.
            It updates the TextView with audio's speaker, confidence and transcription.
            '''

            count = 0
            empty_count = 0
            while self.stop_thread_t2:
                print("Empty Count :",empty_count)
                try:
                    # Saving files to Live segment.
                    cwd = os.getcwd()
                    root_path = cwd + '\\Samples\\' +'Live_Segments\\'
                    output_str = "Output_"+str(count)+"\\"
                    print(root_path+output_str)
                    if glob.glob(root_path+output_str):
                        count = count + 1
                        list_chunk = glob.glob(root_path + output_str+"*.wav")
                        empty_count = 0
                        #Sending chunk to idenify function to get transcription,confidence and speaker.
                        identify(list_chunk)
                        # Add the transcription to display window and dump to txt file.
                        for i in range(len(self.CHUNK_DATA_OBJECTS)):
                            if self.CHUNK_DATA_OBJECTS[i].speaker != '00000000-0000-0000-0000-000000000000':
                                line = logData(self.CHUNK_DATA_OBJECTS[i].count, self.profile_info[self.CHUNK_DATA_OBJECTS[i].speaker],self.CHUNK_DATA_OBJECTS[i].speech_to_text,self.CHUNK_DATA_OBJECTS[i].confidence)
                                display.config(state="normal")
                                display.insert('end','\n'+line+'\n')
                                display.config(state="disable")
                            else:
                                line = logData(self.CHUNK_DATA_OBJECTS[i].count, "UserNotRecognisied" ,self.CHUNK_DATA_OBJECTS[i].speech_to_text,"NA")
                                display.config(state="normal")
                                display.insert('end','\n'+line+'\n')
                                display.config(state="disable")
                        self.CHUNK_DATA_OBJECTS = []
                    else:
                        raise Exception
                except Exception as e:
                    # If no folder is found for continuous two times, then stop transcription.
                    if empty_count == 2:
                        self.stop_thread_t2 = False
                    print("Cannot find the data Folder sleeping for 10 sec:",str(e))
                    empty_count = empty_count + 1
                    time.sleep(12)
            print("Done Transcription")
            if self.rec_start == 1:
                # Dumping files and changing buttons.
                self.rec_start = 0
                cwd = os.getcwd()
                today = datetime.now()
                today = today.strftime("%d-%m-%Y_%H-%M-%S")
                destination = cwd+"\\Transcriptions\\"+str(today)+".txt"
                source = cwd + "\\Dump.txt"
                try:
                    os.rename(source, destination)
                except FileNotFoundError:
                    messagebox.showerror("ERROR", "Unable to move transcription file. Please look for transcription at Dump.text")
                for the_file in os.listdir(cwd + '\\Samples\\' +'Live_Segments'):
                    file_path = os.path.join(cwd + '\\Samples\\' +'Live_Segments', the_file)
                    shutil.rmtree(file_path)
            start_btn.config(state="normal")
            stop_rec_btn.config(state="disable")
            stop_trans_btn.config(state="disable")
            backButton.config(state='normal')
            textLabel_1.configure(text="Transcription Stopped!")
            textLabel_2.configure(text="")

        def first_call():
            '''The function to check intenet connectivity  and call the threads of audio recording and live transcription.'''

            pickle_in = open("profile_selected.pickle","rb")
            self.profile_info = pickle.load(pickle_in)
            pickle_in.close()
            try:
                # Checking connection to Internet.
                ping = url.urlopen("https://www.google.com/", timeout=1)
                print("Connected")
            except urllib.error.URLError:
                print("not Connected")
                messagebox.showerror("NO Connection", "Connect to Internet")
                return
            self.stop_thread_t1 = True
            self.stop_thread_t2 = True
            #Starting record and transcription thread.
            t1 = threading.Thread( target = record)
            t1.start()
            t2 = threading.Thread( target = transcription)
            t2.start()

        def second_call():
            '''The function to stop the live audio recording.'''

            # Stop the record thread.
            self.stop_thread_t1 = False
            textLabel_1.configure(text="\n 'Stop Button' Pressed! Wait for few seconds ")
            stop_rec_btn.config(state="disable")

        def third_call():
            '''The functiont to stop the thread of transcription.'''

            # Stop the transcription thread.
            self.stop_thread_t2 = False
            stop_trans_btn.config(state="disable")
            textLabel_1.configure(text="\n 'Final Stop Button' Pressed! Wait for few seconds ")

        def fourth_call():
            '''The function to delete content of TextView once we go back to previous frame.'''

            textLabel_1.configure(text="Press Start Button to start recording")
            display.config(state='normal')
            display.delete(1.0,'end')
            display.config(state='disable')
            controller.show_frame("SelectUsers")


        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Live Transciption", font=controller.title_font)
        title.place(x=820, y = 30, anchor='center')

        textLabel_1 = tk.Label(self, text="Press Start Button to start recording")
        textLabel_1.place(x=820, y=120, anchor='center')
        textLabel_2 = tk.Label(self, text="")
        textLabel_2.place(x=120, y=70, anchor='center' )

        sb = tk.Scrollbar(self)
        display = tk.Text(self)
        sb.pack(side='right', fill='y')
        display.pack(side='left', fill= 'x')
        sb.config(command=display.yview)
        display.config(yscrollcommand=sb.set)
        display.config(state='disable')
        display.pack(fill = "x", ipady=10)

        start_btn = tk.Button(self, text="START",command=first_call ,width = 20, height = 5)
        start_btn.place(x=820, y=200, anchor = 'center')
        stop_rec_btn = tk.Button(self, text="STOP Recording!",command=second_call,width = 20, height = 5,state="disable")
        stop_rec_btn.place(x=820, y=325, anchor = 'center')
        stop_trans_btn = tk.Button(self, text="STOP Transciption!",command=third_call, width = 20, height= 5, state="disable" )
        stop_trans_btn.place(x=820, y=450, anchor = 'center')
        backButton = tk.Button(self, text="Go Back to Selection", width=65,command=fourth_call)
        backButton.pack(side='bottom', pady=10)
