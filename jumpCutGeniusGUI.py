# Ours
import videoProcessingTools
import cleanVoiceInterface
import jsonParser

# Not ours
import os

def choose_file(filepath):
    if filepath:
        
        tempAudioFilename = videoProcessingTools.mp3_from_mp4(filepath)
        
        signed_url = cleanVoiceInterface.get_signed_cleanvoice_url(tempAudioFilename)  #get signed url for uploading to
        
        cleanVoiceInterface.upload_file(signed_url, tempAudioFilename)  #upload to url
        
        edit_id = cleanVoiceInterface.requestEditToAudio(signed_url)
        
        returned_edit_info = cleanVoiceInterface.retrieveEditInformation(edit_id)

        myJson = returned_edit_info.json()["result"]["edits"]["edits"]
            
        parsedJson = jsonParser.parse_json_to_2d_time_array(myJson)
            
        output_filename = str("OutputContent/" + os.path.basename(filepath))
        output_filename = os.path.splitext(output_filename)[0] + ".mp4"
            
        videoProcessingTools.editVideo(parsedJson, filepath, output_filename)
        
        print(parsedJson)
            
#def get_file_path(self):
    #return self.filepath