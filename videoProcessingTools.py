import subprocess
import requests
import os
import json
import sys



def mp3_from_mp4(input_filename):
    
    output_filename = str("intermediaryContent/"+ os.path.basename(input_filename))
    output_filename = os.path.splitext(output_filename)[0] + ".mp3"
    
    
    subprocess.call(["ffmpeg", "-y", "-i", input_filename, output_filename], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    
    return output_filename