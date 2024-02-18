#OURS
import videoProcessingTools
import cleanVoiceInterface
import jsonParser

#NOT OURS
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import threading

class GUI:
      
    def __init__(self):
       self.root = tk.Tk()
       self.root.title("JumpCut Genius")
       self.root.geometry("1000x800")
       self.root.columnconfigure(0, weight=1)
       self.root.rowconfigure(1, weight=1)
       self.filepath = None  # Initialize filepath attribute

    def runGUI(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=10)
        style.configure("TLabel", font=("Segoe UI", 10))

        choose_file_button = ttk.Button(self.root, text="Choose MP4 File", command=self.choose_file)
        choose_file_button.grid(column=0, row=0, pady=20, padx=20)

        self.chosen_file_label = ttk.Label(self.root, text="No file selected", wraplength=480)
        self.chosen_file_label.grid(column=0, row=1, pady=10, padx=20, sticky="ew")
        
        # Status label to communicate with the user
        self.status_label = ttk.Label(self.root, text="Status: Waiting for action", wraplength=480)
        self.status_label.grid(column=0, row=2, pady=10, padx=20, sticky="ew")

        self.root.mainloop()

    def choose_file(self):
        self.filepath = askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.filepath:
            self.chosen_file_label.config(text=self.filepath)  # Update label with chosen file path
            # Run the processing in a separate thread
            threading.Thread(target=self.process_video, args=(self.filepath,)).start()

    def process_video(self, filepath):
        self.update_status("Status: Processing video to audio...")
        tempAudioFilename = videoProcessingTools.mp3_from_mp4(filepath)
        
        self.update_status("Status: Generating signed URL...")
        signed_url = cleanVoiceInterface.get_signed_cleanvoice_url(tempAudioFilename)

        self.update_status("Status: Uploading audio file...")
        cleanVoiceInterface.upload_file(signed_url, tempAudioFilename)

        self.update_status("Status: Editing out the garbage...")
        edit_id = cleanVoiceInterface.requestEditToAudio(signed_url)

        self.update_status("Status: downloading edit instructions...")
        returned_edit_info = cleanVoiceInterface.retrieveEditInformation(edit_id)

        self.update_status("Status: editing video now...")

        print(returned_edit_info)

    
        #myJson = returned_edit_info.json()["result"]["edits"]["edits"]
        #print(myJson)
        
        #parsedJson = jsonParser.parse_json_to_2d_time_array(myJson)
        #print(parsedJson)
        #print("JSON PRINTED")

    def update_status(self, message):
        # Ensure the status update is performed in the main thread
        self.status_label.config(text=message)
        self.status_label.update_idletasks()
            
    def get_file_path(self):
        return self.filepath