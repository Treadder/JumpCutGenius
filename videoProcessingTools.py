import subprocess
import requests
import os
import json
import sys
import moviepy


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




from moviepy.editor import VideoFileClip, concatenate_videoclips

def transform_array(array_2d,videoinput):
    video = VideoFileClip(videoinput)
    end = video.duration
    # Initialize the new array with the first row
    transformed_array = [[0, array_2d[0][0]]]
    
    # Iterate over the original array
    for i in range(len(array_2d) - 1):
        # For each row, add a new row to the transformed array
        transformed_array.append([array_2d[i][1], array_2d[i + 1][0]])
    
    # Add the final row with the constant 13.14
    transformed_array.append([array_2d[-1][1], end])

    print(transformed_array)
    
    return transformed_array
    



def editVideo(array_2d, videoInput, videoOutPut):
    video = VideoFileClip(videoInput)

    shiftedArray = transform_array(array_2d, videoInput)

    clips = []
    clip = 0

    for row in shiftedArray:
        start = row[0]
        end = row[1]
        print("clip time seconds- ","start:",start,"end:",end)
        cutClip = video.subclip(start,end)
        clips.append(cutClip)
        clip += 1

    finalClip = concatenate_videoclips(clips)
        
    cliptowrite = finalClip
    cliptowrite.write_videofile(videoOutPut,ffmpeg_params=['-crf','18', '-aspect', '9:16'])
    #stack overflow with paramiter changes
    #https://stackoverflow.com/questions/75656843/why-does-moviepy-stretch-my-output-after-cutting-and-putting-back-together-a-vid/75657002#75657002