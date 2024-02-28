# Ours
import videoProcessingTools
import cleanVoiceInterface
import jsonParser

# Not ours
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import os

class GUI:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JumpCut Genius")
        self.root.geometry("1000x600")  # Slightly reduced for a more compact look
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.filepath = None  # Initialize filepath attribute

        # Set custom colors
        self.primary_color = "#4a7abc"  # A pleasant blue
        self.secondary_color = "#ffffff"  # White for contrast
        self.accent_color = "#f2f2f2"  # Light grey for backgrounds

        # Apply custom theme
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "light")

    def runGUI(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=10, background=self.primary_color, foreground=self.secondary_color)
        style.configure("TLabel", font=("Segoe UI", 10), background=self.accent_color, foreground=self.primary_color)
        style.configure("TFrame", background=self.accent_color)

        # Main frame for content
        content_frame = ttk.Frame(self.root)
        content_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
        content_frame.columnconfigure(0, weight=1)

        choose_file_button = ttk.Button(content_frame, text="Choose MP4 File", command=self.choose_file)
        choose_file_button.grid(column=0, row=0, pady=20, padx=20, sticky="ew")

        self.chosen_file_label = ttk.Label(content_frame, text="No file selected", wraplength=480)
        self.chosen_file_label.grid(column=0, row=1, pady=10, padx=20, sticky="ew")
        
        # Status label to communicate with the user
        self.status_label = ttk.Label(content_frame, text="Status: Waiting for action", wraplength=480)
        self.status_label.grid(column=0, row=2, pady=10, padx=20, sticky="ew")

        self.root.mainloop()

    def choose_file(self):
        self.filepath = askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.filepath:
            
            self.chosen_file_label.config(text=self.filepath)  # Update label with chosen file path
            
            self.status_label.config(text="Status: Processing video to audio...")
            print(self.filepath)
            print(self.chosen_file_label)
            tempAudioFilename = videoProcessingTools.mp3_from_mp4(self.filepath)
            
            self.status_label.config(text="Status: Generating signed URL...")
            signed_url = cleanVoiceInterface.get_signed_cleanvoice_url(tempAudioFilename)  #get signed url for uploading to
            
            self.status_label.config(text="Status: Uploading audio file...")
            cleanVoiceInterface.upload_file(signed_url, tempAudioFilename)  #upload to url
            
            self.status_label.config(text="Status: Editing out the garbage....")
            edit_id = cleanVoiceInterface.requestEditToAudio(signed_url)
            
            self.status_label.config(text="Status: downloading edit instructions....")
            returned_edit_info = cleanVoiceInterface.retrieveEditInformation(edit_id)

            myJson = returned_edit_info.json()["result"]["edits"]["edits"]
            
            parsedJson = jsonParser.parse_json_to_2d_time_array(myJson)
            
            self.status_label.config(text="Status: Editing video....")
            
            output_filename = str("OutputContent/" + os.path.basename(self.filepath))
            output_filename = os.path.splitext(output_filename)[0] + ".mp4"
            
            videoProcessingTools.editVideo(parsedJson, self.filepath, output_filename)
        
            print(parsedJson)
            
    def get_file_path(self):
        return self.filepath