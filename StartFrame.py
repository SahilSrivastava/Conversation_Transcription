import tkinter as tk

class StartPage(tk.Frame):
    '''The starting frame of the app.'''

    def __init__(self, parent, controller):
        '''
        The constructor for StartPage class. It defines basic structure of this frame.

        Parameters:
            parent : It represents a widget to act as the parent of the current object.
            controller : It represents some other object that is designed to act as a common point of interaction for several pages of widgets.
        '''

        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Welcome to Audio Transcription", font=controller.title_font)
        add_prof_btn = tk.Button(self, text="Add a New Speaker Profile",
                            command=lambda: controller.show_frame("AddProfile"),
                            width = 40, height = 5)
        rem_prof_btn = tk.Button(self, text="Delete a Speaker Profile",
                            command=lambda: controller.show_frame("RemoveProfile"),
                            width = 40, height = 5)
        trans_btn = tk.Button(self, text="Process an Audio File",
                            command=lambda: controller.show_frame("SelectUsers"),
                            width = 80, height = 5)

        title.place(x=512, y = 30, anchor='center')
        add_prof_btn.place(x=312, y=200, anchor = 'center')
        rem_prof_btn.place(x=712, y=200, anchor = 'center')
        trans_btn.place(x=512, y=400, anchor = 'center')
