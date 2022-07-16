import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import SpotifyPlaylist, converter

class ConverterWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        # self.AVoption = 2
        self.spotify_url = ""

        self.title('Spotify Converter')
        window_width = 330
        window_height = 150
        #self.resizable(0,0)
        
        #center screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.grid_columnconfigure(0,weight=3)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.create_widgets()
        
        
    def create_widgets(self):
        self.browse_button = ttk.Button(self,text="Browse Folder",command=self.browseFolder)
        self.browse_button.grid(column=2,row=0)

        # self.audio_button = ttk.Button(self,text="Audio",command=())
        # self.audio_button.grid(column=2,row=1)

        # self.video_button = ttk.Button(self,text="Video",command=())
        # self.video_button.grid(column=2,row=2)

        self.input_txtbox = tk.Text(self,height=1,width=15)
        self.input_txtbox.grid(column=0,row=0)

        self.convert_button = ttk.Button(self,text="Convert",command=self.ConvertButtonAction)
        self.convert_button.grid(column=0,row=1)

        self.info = tk.Label(self,text="1. Enter Spotify playlist URL")
        self.info.grid(column=0,row=3,sticky="W")
        self.info1 = tk.Label(self,text="2. Browse destination folder")
        self.info1.grid(column=0,row=4,sticky="W")
        self.info2 = tk.Label(self,text="3. Convert")
        self.info2.grid(column=0,row=5,sticky="W")
    def browseFolder(self):
        self.folder_path = filedialog.askdirectory()
        print(self.folder_path)
    
    def change_trace(self):
        new_state = "normal"
        if (self.input_txtbox.get()==""):
            new_state = "disabled"
        self.convert_button.state([new_state])
    def ConvertButtonAction(self):
        self.spotify_url = self.input_txtbox.get(1.0, "end-1c")
        if (self.spotify_url == ""):
            print("Link error")
            messagebox.showerror("ERROR","Enter valid URL")
        elif (self.folder_path==""):
            messagebox.showerror("ERROR","Browse folder destination before converting")
        else:
            print("Converting spotify playlist")
            try:
                failed_songs = SpotifyPlaylist.downloadTRACKS(self.spotify_url,self.folder_path)
                messagebox.showinfo("Done","Finished downloading playlist")
            except:
                messagebox.showerror("ERROR","URL did not work")
                return -1
            if (len(failed_songs)==0):
                return 1
            else:
                x = 1
                for i in failed_songs:
                    messagebox.showerror(f"{x}. ERROR", f"Failed to download {i}")
                    x += 1
                return -1

if __name__ == "__main__":
    window1 = ConverterWindow()
    window1.mainloop()