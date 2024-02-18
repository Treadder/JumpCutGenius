import subprocess
import requests
import os
import json
import sys

import shutil  # Import shutil for high-level file operations

def clear_intermediary_content():
    folder_path = 'intermediaryContent/'
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove all contents of the folder
        shutil.rmtree(folder_path)
        # Recreate the folder
        os.makedirs(folder_path)
    else:
        # If the folder doesn't exist, create it
        os.makedirs(folder_path)

def mp3_from_mp4(input_filename):
    # Clear the intermediary content folder at the start
    
    output_filename = str("intermediaryContent/" + os.path.basename(input_filename))
    output_filename = os.path.splitext(output_filename)[0] + ".mp3"
    
    subprocess.call(["ffmpeg", "-y", "-i", input_filename, output_filename],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    
    return output_filename
