import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import SpotifyPlaylist

class ConverterWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.AVoption = 2
        self.video_url = ""

        self.title('Converter')
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

        self.audio_button = ttk.Button(self,text="Audio",command=self.AudioOption)
        self.audio_button.grid(column=2,row=1)

        self.video_button = ttk.Button(self,text="Video",command=self.VideoOption)
        self.video_button.grid(column=2,row=2)

        self.input_txtbox = tk.Text(self,height=1,width=15)
        self.input_txtbox.grid(column=0,row=0)

        self.convert_button = ttk.Button(self,text="Convert",command=self.ConvertButtonAction)
        self.convert_button.grid(column=0,row=1)

        self.info = tk.Label(self,text="1. Enter video/playlist URL")
        self.info.grid(column=0,row=3,sticky="W")
        self.info1 = tk.Label(self,text="2. Browse destination folder")
        self.info1.grid(column=0,row=4,sticky="W")
        self.info2 = tk.Label(self,text="3. Select video/audio then convert")
        self.info2.grid(column=0,row=5,sticky="W")
    def browseFolder(self):
        self.folder_path = filedialog.askdirectory()
        print(self.folder_path)

    # def AudioOption(self):
    #     self.AVoption = 1
    #     print("Audio",self.AVoption)

    # def VideoOption(self):
    #     self.AVoption = 0
    #     print("Video",self.AVoption)
    
    def change_trace(self):
        new_state = "normal"
        if (self.input_txtbox.get()==""):
            new_state = "disabled"
        self.convert_button.state([new_state])
    def ConvertButtonAction(self):
        self.video_url = self.input_txtbox.get(1.0, "end-1c")
        if (self.video_url == ""):
            print("Link error")
            messagebox.showerror("ERROR","Enter valid URL")
        elif (self.folder_path==""):
            messagebox.showerror("ERROR","Browse folder destination before converting")
        elif (self.AVoption==2):
            messagebox.showerror("ERROR","Select video/audio before converting")

        if (converter.download_video(self.video_url,self.folder_path,self.AVoption)==-1):
            converter.download_playlist(self.video_url,self.folder_path,self.AVoption)
            messagebox.showinfo("Done",f"Playlist finished downloading to {self.folder_path}")
        else:
            messagebox.showinfo("Done",f"Video finished downloading to {self.folder_path}")


if __name__ == "__main__":
    window1 = ConverterWindow()
    window1.mainloop()