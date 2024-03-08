#our written imports
import videoProcessingTools

#our non-written imports
import requests
import json
import time


#api_key = "WEWhZJ5U9jpoFofqYgrCm7hLrPYgttB2"
#api_key = "97xL22Ayz9PWs8kYUeA4yVUK9UmdJZi9"
#api_key = "7i9QacfrR6CtEKFA8q92BU6BSKKiR7fj"
api_key = "Hj4F4msYEYUhKgyCfDpMWuVeGSPTXKHj"



def get_signed_cleanvoice_url(upload_filename):
    
    #upload_filename = videoProcessingTools.mp3_from_mp4("testAgain.mp4")
    url = 'https://api.cleanvoice.ai/v1/upload?filename=' + upload_filename
    headers = {'X-API-Key': api_key}

    response = requests.post(url, headers=headers)
    signed_url = response.json()['signedUrl']

    print("")
    print("RAN get_signed_cleanvoice_url. Response:")
    print(response)
    print("")
    
    
    
    return signed_url
    


    
def upload_file(signed_url, upload_filename):
    
    upload_file = open(upload_filename, "rb")

    requests.put(signed_url, data=upload_file)
    
    print("")
    print("RAN upload_file")
    print("")
    



def requestEditToAudio(signed_url):
    
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
    
    print("")
    print("requestEditToAudio response:")
    print(response)
    print("")
    
    return edit_id



def retrieveEditInformation(edit_id):
    
    url = "https://api.cleanvoice.ai/v1/edits/" + edit_id

    headers = {
        "X-Api-Key": api_key
    }

    print("retreiving edit information. It could take a bit:")
    
    status = "PROGRESS"         #this is so we don't finish this function till wehave successfully gotten the edit deets back
    response = None
    
    while(status != "SUCCESS"):
        response = requests.get(url, headers=headers)    
        status = response.json()["status"]
        print("status:" + status)
        time.sleep(5)
        
    time.sleep(3)
    response = requests.get(url, headers=headers)   #this is insane but it works don't ask questions just accept it. It's fine.
    return response

























    
