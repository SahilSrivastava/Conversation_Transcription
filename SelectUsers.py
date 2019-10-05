from UtilFunctions import *
from tkinter import messagebox
import time, pickle
import tkinter as tk


class SelectUsers(tk.Frame):
    '''The class to select speaker profiles we need for audio transcription.'''

    def __init__(self, parent, controller):
        '''
        The constructor of SelectUsers class that define basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        def on_show_frame(self):
            '''The function to call the function to update the list of enrolled speaker profiles.'''

            update_list(enrolled_list,"list")

        def get_selected():
            '''
            The function to get the list of selected users and update that list on other listview.
            If no user is selected than error is displayed.
            '''
            # Fetch the names selected in the list
            all_items = enrolled_list.get(0, tk.END)
            sel_idx = enrolled_list.curselection()
            sel_list = [all_items[item] for item in sel_idx]
            # Printing error if no name is selected
            if len(sel_list)==0:
                messagebox.showerror("ERROR", "Please select profiles")
                selected_prof.config(state="normal")
                selected_prof.delete(1.0,'end')
                selected_prof.config(state="disable")
                live_btn.config(state="disable")
                import_file_btn.config(state="disable")
                return
            # Opening pickle and finding the respective keys of names selected by user.
            pickle_in = open("my_dict.pickle","rb")
            in_dict = pickle.load(pickle_in)
            pickle_in.close()
            p={}
            for k,v in in_dict.items():
                if v in sel_list:
                    p[k]=v
            # Dumping those key-name pair to new pickle file
            pickle_out = open("profile_selected.pickle","wb")
            pickle.dump(p,pickle_out)
            pickle_out.close()
            speaker_count = 1
            # Updating the ListView which shows selected user.
            selected_prof.config(state="normal")
            selected_prof.delete(1.0,'end')
            for value in p.values():
                selected_prof.insert('end',str(speaker_count)+". "+value+'\n')
                speaker_count = speaker_count + 1
            selected_prof.config(state="disable")
            live_btn.config(state="normal")
            import_file_btn.config(state="normal")


        tk.Frame.__init__(self, parent)
        self.controller = controller
        try:
            pickle_in = open("my_dict.pickle","rb")
            in_dict = pickle.load(pickle_in)
            pickle_in.close()
        except :
            in_dict = {}

        label_1 = tk.Label(self, text="Please Select Profiles", font=controller.title_font)
        label_1.place(x=125, y=100, anchor ='center')
        label_2 = tk.Label(self, text="Selected Profiles", font=controller.title_font)
        label_2.place(x=900, y=100, anchor ='center')

        enrolled_list = tk.Listbox(self,selectmode='multiple',width=30, height=25)
        enrolled_list.place(x=125, y=325, anchor ='center')
        try:
            for value in in_dict.values():
                enrolled_list.insert('end',value)
        except :
            pass
        selected_prof = tk.Text(self,width=20, height=25, state = "disable")
        selected_prof.place(x=900, y=325, anchor="center" )

        select_btn = tk.Button(self, text="SELECT",command=get_selected ,width = 20, height = 5)
        select_btn.place(x=512, y=200, anchor = 'center')
        live_btn = tk.Button(self, text="Transcription By Mic",state="disable",command=lambda: controller.show_frame("Identify") ,width = 20, height = 5)
        live_btn.place(x=512, y=300, anchor = 'center')
        import_file_btn = tk.Button(self, text="Transcription By File",state="disable",command=lambda: controller.show_frame("ImportIdentify") ,width = 20, height = 5)
        import_file_btn.place(x=512, y=400, anchor = 'center')
        backButton = tk.Button(self, text="Go Back to Main Menu", width=65,command=lambda: controller.show_frame("StartPage"))
        backButton.pack(side='bottom', pady=10)

        self.bind("<<ShowFrame>>", on_show_frame)
