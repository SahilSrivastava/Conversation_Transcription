from AllApiFiles import *
from UtilFunctions import *
from datetime import datetime
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk
import urllib.request as url
import threading, os, time, glob, pickle, urllib


instance = Value()
class ImportIdentify(tk.Frame):
    '''The class to do audio transcription by importing a already recorded audio file.'''

    thread_t1 = True
    j = 0
    CHUNK_DATA_OBJECTS = []
    profile_info = {}
    rec_start = 0
    empty_select = 0

    def __init__(self, parent, controller):
        '''
        The constructor of ImportIdentify class that define basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        def importFile():
            '''The function to import a audio file and do the segementation of audio file.'''

            try:
                # Function to import a file from computer.
                IMPORTED_FILE = askopenfilename()
                print("Selected file: ", IMPORTED_FILE)
                display.config(state='normal')
                display.delete(1.0, 'end')
                display.insert('end', "Processing. Please Wait")
                display.config(state='disable')
                import_button.config(state="disable")
                stop_button.config(state="disable")
                backButton.config(state="disable")
                # Finding duration of the imported audio.
                total_duration = get_duration(IMPORTED_FILE)
                print("Duration of Imported Audio is: ",total_duration)
                # Segmenting the audio into chunks.
                audio_segments(self.j,total_duration,IMPORTED_FILE,"import")
                # Variable which is 1 if import is done successfully
                self.rec_start = 1
                display.config(state='normal')
                display.delete(1.0, 'end')
                display.insert('end', "Segmentation Done")
                display.config(state='disable')
                stop_button.config(state="normal")
            # Error in case no file is selected.
            except FileNotFoundError:
                display.config(state='normal')
                display.delete(1.0, 'end')
                display.insert('end', "Upload a wav file to Start \n (Encoding: \t PCM Sample rate: 16k \t Sample format: 16 bit \t Chanel: Mono) ")
                display.config(state='disable')
                messagebox.showerror("ERROR", "Please select File")
                self.rec_start = 0
                import_button.config(state="normal")
                stop_button.config(state="disable")
                backButton.config(state="normal")
                return 1

        def identify(list_chunk):
            '''
            The function to recieve a chuck of audio list and process each of the audio file and tell it's transcription, speaker and confidence.

            Parameters:
                list_chunk : The list of segmented audiofiles recieved from 10 second audio files.
            '''

            display.config(state="normal")
            display.delete(1.0, 'end')
            display.config(state="disable")
            print("Starting Process")
            speech_data = ''
            speaker_data = ''
            # Opening the pickle file to fetch the selected users.
            pickle_in = open("profile_selected.pickle","rb")
            profile_id_list_all = pickle.load(pickle_in)
            pickle_in.close()
            try:
                # A list to fetch keys of all selected users.
                profile_id_list = [keys for keys in profile_id_list_all.keys()]
            except Exception as e:
                print("Error in getting profile Ids",str(e))
            print(profile_id_list)
            # Using each chunk and the send for transcription.
            for each_chunk in list_chunk:
                if self.thread_t1:
                    # Transcription will be done only when each chunk is greater than one second.
                    if get_duration(each_chunk) > 1.0:
                        instance.API_RATE += 1
                        if(instance.API_RATE < 10):
                            # Count of each chunk.
                            instance.COUNT += 1
                            try:
                                # Get the transcription of each chunk.
                                speech_data = speech_recognize_once_from_file(each_chunk)
                            except Exception as e:
                                print("Exception in speech to text",str(e))
                                print("Skipping chunk: {}".format(each_chunk))
                                continue
                            try:
                                print("identifying Speaker")
                                # Finding the speaker id and the confidence.
                                speaker_object = identify_file(OCM_API,each_chunk,"True",profile_id_list)
                                speaker_data = speaker_object.get_identified_profile_id()
                                confidence = speaker_object.get_confidence()
                            except Exception as e:
                                print("Exception in speaker",str(e),)
                                print("Speaker for wav{} has set to Blank".format(each_chunk))
                                speaker = "NULL"
                                continue
                            for i in range(len(self.CHUNK_DATA_OBJECTS)):
                                if self.CHUNK_DATA_OBJECTS[i].speaker != '00000000-0000-0000-0000-000000000000':
                                    # A function is called to Dump the transcription in txt file.
                                    line = logData(instance.COUNT, self.profile_info[self.CHUNK_DATA_OBJECTS[i].speaker],self.CHUNK_DATA_OBJECTS[i].speech_to_text,self.CHUNK_DATA_OBJECTS[i].confidence)
                                    # Putting the transcription in display window.
                                    display.config(state="normal")
                                    display.insert('end','\n'+line+'\n')
                                    display.config(state="disable")
                                else:
                                    # If the user is not recognised then put name as UserNotRecognisied and display transcription.
                                    line = logData(instance.COUNT, "UserNotRecognisied" ,self.CHUNK_DATA_OBJECTS[i].speech_to_text,"NA")
                                    display.config(state="normal")
                                    display.insert('end','\n'+line+'\n')
                                    display.config(state="disable")
                                self.CHUNK_DATA_OBJECTS = []
                            self.CHUNK_DATA_OBJECTS.append(ChunkDataList(instance.COUNT,speaker_data,speech_data,confidence))
                        else:
                            instance.API_RATE = 0
                            time.sleep(12)
                    else:
                        print("Skipping Chunk" , each_chunk, get_duration(each_chunk))
                        continue
                else:
                    break

        def transcription():
            '''
            The function to fetch the segmented audio files from a folder and send to 'identity' function as audio list.
            It updates the TextView with audio's speaker, confidence and transcription.
            '''

            display.config(state='normal')
            display.delete(1.0, 'end')
            display.config(state="disable")
            textLabel_2.configure(text="Transciption Started")
            try:
                # Path to fetch the chunks
                cwd = os.getcwd()
                root_path = cwd + '\\Samples\\Import_chunks\\'
                if glob.glob(root_path):
                    list_chunk = glob.glob(root_path + "*.wav")
                    # Sending all chunks to get transcription.
                    identify(list_chunk)
                else:
                    raise Exception
            except Exception as e:
                print("Cannot find the data Folder sleeping for 10 sec:",str(e))
                time.sleep(12)
            # If audio file is imported successfully then call the below code.
            if self.rec_start == 1:
                self.rec_start = 0
                # Get current datetime folder to move txt file to that folder
                cwd = os.getcwd()
                today = datetime.now()
                today = today.strftime("%d-%m-%Y_%H-%M-%S")
                destination = cwd+"\\Transcriptions\\"+str(today)+".txt"
                source = cwd + "\\Dump.txt"
                # Changing the destination of txt file.
                os.rename(source, destination)
                # Removing the chunks
                for the_file in os.listdir(cwd + '\\Samples\\' +'Import_chunks'):
                    file_path = os.path.join(cwd + '\\Samples\\' +'Import_chunks', the_file)
                    os.unlink(file_path)
            instance.COUNT = 0
            print("Transcription Complete")
            display.config(state='normal')
            display.insert('end', "DONE TRANSCRIPTION")
            display.config(state="disable")
            textLabel_2.configure(text="Transciption Completed")
            import_button.config(state="normal")
            stop_button.config(state="disable")
            backButton.config(state="normal")

        def first_call():
            '''The function to check internet connectivity and a fuction to import file and then call a thread to call 'transcription' function.'''

            # Opening pickle file and loading the profiles selected for transcription.
            pickle_in = open("profile_selected.pickle","rb")
            self.profile_info = pickle.load(pickle_in)
            pickle_in.close()
            self.thread_t1 = True
            try:
                # Check for internet connection
                ping = url.urlopen("https://www.google.com/", timeout=1)
                print("Connected")
            except urllib.error.URLError:
                print("not Connected")
                messagebox.showerror("NO Connection", "Connect to Internet")
                return
            # If no file is selected then return, else continue.
            empty_select = importFile()
            if empty_select == 1:
                print("NO file")
                return
            # Once segmentation is done, transcription thread is carried out.
            t2 = threading.Thread( target = transcription)
            t2.start()

        def second_call():
            '''The fuction to stop the execution of thread t1'''

            # Thread to stop the transcription.
            self.thread_t1 = False
            stop_button.config(state="disable")
            textLabel_2.configure(text="'Final Stop' backButton pressed. Wait for few Seconds!")
            print("Final Stop button is pressed.")

        def third_call():
            '''The function to delete content of TextView once we go back to previous frame.'''

            # While retuening to previous frame, remove the text from display window and switch to selected frame.
            display.config(state='normal')
            display.delete(1.0, 'end')
            display.config(state="disable")
            controller.show_frame("SelectUsers")


        tk.Frame.__init__(self, parent)
        self.controller = controller

        textLabel_1 = tk.Label(self, text="Audio Transciption", font=controller.title_font)
        textLabel_1.pack(side="top", fill="x", pady=10)
        textLabel_2 = tk.Label(self, text="")
        textLabel_2.place(x=150, y=90, anchor='center' )

        sb = tk.Scrollbar(self)
        sb.pack(side='right', fill='y')
        display = tk.Text(self)
        display.insert('end', "Upload a wav file to Start \n (Encoding: \t PCM Sample rate: 16k \t Sample format: 16 bit \t Chanel: Mono) ")
        display.config(state='disabled')
        display.pack(side='left', fill= 'x')
        display.pack(fill = "x", ipady=10)
        sb.config(command=display.yview)
        display.config(yscrollcommand=sb.set)

        backButton = tk.Button(self, text="Go Back to Selection", width = 20,command=third_call)
        backButton.pack(side='bottom', fill = "y", pady = 10)
        import_button = tk.Button(self, text="Import a Audio file", width=20,command=first_call)
        import_button.pack(side='top', fill ='y', pady = 10)
        stop_button = tk.Button(self, text="Final Stop", width=20,state="disable",command=second_call)
        stop_button.pack(side='top', fill ='y', pady = 10)
