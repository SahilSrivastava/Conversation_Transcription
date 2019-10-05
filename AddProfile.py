from tkinter import ttk
from tkinter import messagebox
from AllApiFiles import *
from UtilFunctions import *
from RecordingFunction import *
import urllib
import tkinter as tk
import urllib.request as url
import threading, os, time


class AddProfile(tk.Frame):
    '''The class to add a new speaker profile.'''

    def __init__(self, parent, controller):
        '''
        The constructor of AddProfile class that define basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        def on_show_frame(self):
            '''The function to call the function to update the list of enrolled speaker profiles.'''

            # Update the list box with profiles enrolled
            update_list(enrolled_list,"text")

        def createProfile():
            '''The function to create a new user profile after the recording of the new speaker is completed.'''


            createButton.config(state="disabled")
            textLabel_1.configure(text="Please wait for few seconds.")
            textLabel_2.configure(text="")
            try:
                # Loading the pickle file
                pickle_in = open("my_dict.pickle","rb")
                in_dict = pickle.load(pickle_in)
                pickle_in.close()
            except :
                in_dict = {}
            # Get the name enetered in nameEntry box.
            name = nameEntry.get()
            nameEntry.delete(0, 'end')
            nameEntry.config(state = "disable")
            try:
                # If name in namefield is repeated then show the error.
                if name in in_dict.values():
                    messagebox.showerror("Invalid Name", "Entered Name is already present in the List")
                    textLabel_1.configure(text="Recording Done.")
                    textLabel_2.configure(text="Enter name and and press Create Profile to enroll user")
                    createButton.config(state="normal")
                    return
            except :
                pass
            # If name field is empty then show error.
            if name=="":
                messagebox.showerror("Invalid Name", "A valid name is required to proceed")
                textLabel_1.configure(text="Recording Done.")
                textLabel_2.configure(text="Enter name and and press Create Profile to enroll user")
                createButton.config(state="normal")
            else:
                try:
                    #Function to enroll the profile on server.
                    enroll_profile(OCM_API, self.id.get_profile_id(), "output.wav", 'true')
                except:
                    # If any error while enrolling then show error.
                    messagebox.showerror("ERROR", "Press Create Profile again")
                    textLabel_1.configure(text="Please press create button again.")
                    createButton.config(state="normal")
                    return
                # Loading the pickle file, then updating the list and then dumping new list in pickle file.
                try:
                    pickle_in = open("my_dict.pickle","rb")
                    in_dict = pickle.load(pickle_in)
                    in_dict[str(self.id.get_profile_id())] = name
                    pickle_in.close()
                except :
                    in_dict[str(self.id.get_profile_id())] = name
                # Dumping the new updated list to pickle file.
                pickle_out = open("my_dict.pickle","wb")
                pickle.dump(in_dict,pickle_out)
                pickle_out.close()
                # Function that will update the list window once profile is created.
                update_list(enrolled_list,"text")
                textLabel_1.configure(text="Enrollment Done. You can create new profile now.")
                textLabel_2.configure(text="")
                createButton.config(state="disabled")
                recordButton.config(state="normal")
                backButton.config(state="normal")
                nameEntry.config(state = "normal")
                print("Enrollment Done.")

        def _startRecord():
            '''The function to start the audio recording of the new speaker to be enrolled.'''

            nameEntry.config(state = "disable")
            textLabel_1.configure(text="Wait!")
            createButton.config(state="disable")
            recordButton.config(state="disable")
            backButton.config(state="disable")
            try:
                # Function to get the new create profile id.
                self.id = create_profile(OCM_API, LOCALE)
                print(self.id.get_profile_id())
            except:
                # If any error occur then show the error.
                messagebox.showerror("API ERROR", "Error Occured while creating id")
                recordButton.config(state="normal")
                return
            time.sleep(1)
            textLabel_1.configure(text="Recording Started. Speak For 60 Seconds.")
            # Function to record the audio of new speaker for 60 seconds
            audio_record(0,"output.wav",60,progress)
            textLabel_1.configure(text="Recording Done")
            textLabel_2.configure(text="Press Create Button to enroll the speaker's profile.")
            createButton.config(state="normal")
            nameEntry.config(state = "normal")

        def first_call():
            '''The function to check internet connectivity and start the thread of audio recording.'''

            try:
                # Checking the internet connectivity, if no connection then error is shown and it return.
                ping = url.urlopen("https://www.google.com/", timeout=1)
                print("Connected")
            except urllib.error.URLError:
                print("not Connected")
                messagebox.showerror("NO Connection", "Connect to Internet")
                return
            # Call the thread to start the recording.
            t1 = threading.Thread( target = _startRecord)
            t1.start()

        def second_call():
            '''The function to call the thread to enroll the new profile of recorded speaker.'''

            # Thread to call create profie and enroll into server
            t2 = threading.Thread( target = createProfile)
            t2.start()


        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.id=None

        label_1 = tk.Label(self, text="Page to Add New Speakers", font=controller.title_font)
        label_1.pack(side="top", fill="x", pady=10)
        label_2 = tk.Label(self, text="Profiles Already Enrolled")
        label_2.place(x=125, y=100, anchor ='center')

        nameLabel =tk.Label(self, width=30, text="Enter Speaker Name:")
        nameLabel.place(x=430, y=100, anchor ='center')
        nameEntry = tk.Entry(self)
        nameEntry.place(x=570, y=100, anchor ='center')

        enrolled_list = tk.Text(self,width=30, height=25, state="disable")
        enrolled_list.place(x=125, y=325, anchor ='center')
        sb = tk.Scrollbar(self)
        sb.pack(side='right', fill='y')
        sb.config(command=enrolled_list.yview)
        enrolled_list.config(yscrollcommand=sb.set)

        textLabel_1 = tk.Label(self, text="Press Record Button to record your voice.")
        textLabel_1.place(x=512, y=250, anchor='center')
        textLabel_2 = tk.Label(self, text="")
        textLabel_2.place(x=512, y=450, anchor='center')

        progress = ttk.Progressbar(self, orient = 'horizontal', length = 200)
        progress.place(x=512, y=400, anchor='center')
        progress.config(mode = 'determinate', maximum=int(RATE / CHUNK * 60), value=0)

        recordButton = tk.Button(self, text="Record", width=30,command=first_call)
        recordButton.place(x=512, y=320, anchor='center')
        createButton = tk.Button(self, text="Create Profile",state='disable', width=65,command=second_call)
        createButton.place(x=512, y=500, anchor='center')
        backButton = tk.Button(self, text="Go Back to Main Menu", width=65,command=lambda: controller.show_frame("StartPage"))
        backButton.pack(side='bottom', pady=10)

        self.bind("<<ShowFrame>>", on_show_frame)
