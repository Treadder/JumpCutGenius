#Our Local Imports
import jumpCutGeniusGUI
import cleanVoiceInterface
import videoProcessingTools


#Not our own written imports
import requests
import os
import json
import sys

#%% START GUI AND GET FILE PATH

videoProcessingTools.clear_intermediary_content()
videoProcessingTools.clear_output_content()


appGUI = jumpCutGeniusGUI.GUI()
appGUI.runGUI()

#TODO use moviepie and make this whole thing portable
