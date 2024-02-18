import subprocess
import requests
import os
import json
import sys

#%%BASE VARIABLES

api_key = "WEWhZJ5U9jpoFofqYgrCm7hLrPYgttB2"


#%% FUNCTION TO RIP THE AUDIO FROM THE VIDEO FILE IN THIS DIRECTORY

def convert_video_to_audio_ffmpeg(input_filename):
    
    output_filename = str(os.path.splitext(input_filename)[0]) + ".mp3"
    
    subprocess.call(["ffmpeg", "-y", "-i", input_filename, output_filename], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    
    return output_filename

#%%CONVERT VIDEO TO AUDIO NOW.  NOTE THAT FILENAME MUST NOT HAVE NUMBERS IN IT

upload_filename = convert_video_to_audio_ffmpeg("testAgain.mp4")


#%% GET SIGNED URL TO UPLOAD TO

url = 'https://api.cleanvoice.ai/v1/upload?filename=' + upload_filename
headers = {'X-API-Key': api_key}

response = requests.post(url, headers=headers)
signed_url = response.json()['signedUrl']

print("will upload to: " + signed_url)


#%%UPLOAD AUDIO

upload_file = open(upload_filename, "rb")

requests.put(signed_url, data=upload_file)


#%%REQUEST AN EDIT TO UPLOADED AUDIO

data = {
    "input": {
        "files": [signed_url],
        "config": {
            "send_mail": False,
            "timestamps_only": True,
            "remove_noise": False,
            "mastering:": False,
            "export_edits": True,
            "ignore_music": True,
            "ignore_features": ["STUTTERING"]
            }
    }
}


headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.post("https://api.cleanvoice.ai/v1/edits", json=data, headers=headers)

edit_id = response.json()['id']


#%% RETRIEVE EDIT INFORMAITON

url = "https://api.cleanvoice.ai/v1/edits/" + edit_id

headers = {
    "X-Api-Key": api_key
}

response = requests.get(url, headers=headers)


# %%PARSE JSON FOR EDITING VIDEO. Start, stop format in REVERSE so editing video doesn't mess up timing.

myJson = response.json()["result"]["edits"]["edits"]

#%% PARSE RETURN JSON

def parse_json_to_2d_time_array(json_data):
    try:
        # Extract the 'start' and 'end' times
        time_values_2d = [[edit['start'], edit['end']] for edit in json_data]

        return time_values_2d

    except KeyError as e:
        print(f"Error: Missing key in JSON structure - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


time_array = parse_json_to_2d_time_array(myJson)
time_array.reverse()
