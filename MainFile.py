from StartFrame import *
from AddProfile import *
from SelectUsers import *
from RemoveProfile import *
from TranscriptionLive import *
from TranscriptionByImport import *
from tkinter import font as tkfont
import tkinter as tk


class TIApp(tk.Tk):
    '''This is a class to create tkinter app.'''

    def __init__(self, *args, **kwargs):
        '''The constructor to define the basic attributes of app.'''

        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Transcription and Speaker Identification")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("1024x576")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # Loading various frames of the App.
        for F in (StartPage,AddProfile,RemoveProfile,Identify,ImportIdentify,SelectUsers):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")
    #Function to show a particular frame.
    def show_frame(self, page_name):
        '''The function to show a frame over all other frames.'''

        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

if __name__ == "__main__":
    app = TIApp()
    app.mainloop()
