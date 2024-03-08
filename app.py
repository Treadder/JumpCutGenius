#Our Local Imports
import jumpCutGeniusGUI
import cleanVoiceInterface
import videoProcessingTools


#Not our own written imports
import requests
import os
import json
import sys
from flask import * #importing flask (Install it using python -m pip install flask)
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__) #initialising flask


@app.route("/") #defining the routes for the home() funtion (Multiple routes can be used as seen here)
@app.route("/home")
def home():
    return render_template("home.html") #rendering our home.html contained within /templates

@app.route("/account", methods=["POST", "GET"]) #defining the routes for the account() funtion
def account():
    usr = "<User Not Defined>" #Creating a variable usr
    if (request.method == "POST"): #Checking if the method of request was post
        usr = request.form["name"] #getting the name of the user from the form on home page
        if not usr: #if name is not defined it is set to default string
            usr = "<User Not Defined>"
    return render_template("account.html",username=usr) #rendering our account.html contained within /templates

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        # Save the file to a desired location (e.g., 'uploads' folder)
        file.save(f'./uploads/{filename}')
        filepath =(f'./uploads/{filename}')
        print(filepath)
        videoProcessingTools.clear_intermediary_content()
        videoProcessingTools.clear_output_content()
        jumpCutGeniusGUI.choose_file(filepath)
        return f"File '{filename}' uploaded successfully!"
    return "No file uploaded."


if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True,port=4949) #running flask (Initalised on line 4)
