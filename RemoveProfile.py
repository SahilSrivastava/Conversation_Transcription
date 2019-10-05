from tkinter import messagebox
from AllApiFiles import *
from UtilFunctions import *
import tkinter as tk
import pickle, urllib
import urllib.request as url


class RemoveProfile(tk.Frame):
    '''The class to remove a speaker's profile from the list of already enrolled profiles.'''

    def __init__(self, parent, controller):
        '''
        The constructor of RemoveProfile class that define basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        def on_show_frame(self):
            '''The function to call the function to update the list of enrolled speaker profiles.'''

            # Calling to function to update the list.
            update_list(enrolled_list,"list")

        def get_selected():
            '''The function to check the connection. It also get the selected profile to delete and updated the list.'''

            # Checking the connection to internet.
            try:
                ping = url.urlopen("https://www.google.com/", timeout=1)
                print("Connected")
            except urllib.error.URLError:
                print("not Connected")
                messagebox.showerror("NO Connection", "Connect to Internet")
                return
            # Getting the name selected by the user.
            all_items = enrolled_list.get(0, tk.END)
            sel_idx = enrolled_list.curselection()
            sel_list = [all_items[item] for item in sel_idx]
            # Give error if no profile is selected.
            if len(sel_list)==0:
                messagebox.showerror("ERROR", "Please select a profile")
                return
            # Loading pickle file which contain information of all users.
            pickle_in = open("my_dict.pickle","rb")
            in_dict = pickle.load(pickle_in)
            print(in_dict)
            pickle_in.close()
            # Getting the key of the corresponding name.
            for k,v in in_dict.items():
                if v == sel_list[0]:
                    k_get=k
            # Deleting that key and username from the server.
            delete_profile(OCM_API, str(k_get))
            # Updating the list in the window.
            del in_dict[k_get]
            enrolled_list.delete('0','end')
            for value in in_dict.values():
                enrolled_list.insert('end',value)
            pickle_out = open("my_dict.pickle","wb")
            pickle.dump(in_dict,pickle_out)
            print(in_dict)
            pickle_out.close()


        tk.Frame.__init__(self, parent)
        self.controller = controller
        try:
            pickle_in = open("my_dict.pickle","rb")
            in_dict = pickle.load(pickle_in)
            pickle_in.close()
        except :
            in_dict ={}

        title = tk.Label(self, text="Delete Profile", font=controller.title_font)
        title.pack(side="top", fill="x", pady=10)

        enrolled_list = tk.Listbox(self)
        enrolled_list.pack()
        try:
            for value in in_dict.values():
                enrolled_list.insert('end',value)
        except :
            pass

        textLabel = tk.Label(self, text="Please select a profile to delete.")
        textLabel.place(x=820, y=100, anchor='center')

        delete_btn = tk.Button(self, text="DELETE!",command=get_selected ,width = 20, height = 5)
        delete_btn.place(x=820, y=200, anchor = 'center')
        backButton = tk.Button(self, text="Go Back to Main Menu", width=65,command=lambda: controller.show_frame("StartPage"))
        backButton.pack(side='bottom', pady=10)

        self.bind("<<ShowFrame>>", on_show_frame)
