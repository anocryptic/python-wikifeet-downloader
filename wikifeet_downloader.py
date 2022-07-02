import requests
import re
import json 
import os
import argparse
import sys
import shutil
from inspect import getsourcefile
from os.path import abspath
from pathlib import Path

# using this header to prevent the server from blocking our script, forbidding (403) our access to the website
non_bot_header = {'User-Agent': 'Mozilla/5.0'}

# patterns used to recognize if given url is a valid wikifeet or wikifeetx one
wikifeet_pattern = 'https:\/\/www\.wikifeet\.com\/[a-zA-Z_]+'
wikifeetx_pattern = 'https:\/\/www\.wikifeetx\.com\/[a-zA-Z_]+'

# JSONExtractor class extracts the javascript associative array found in every model html page;
# it contains a lists of every model feet pic and can be interpreted as json data
class JSONExtractor:

    js_variable = "messanger['gdata'] = ["

    def __init__(self, text=""):
        self.text = text

    def set_text(self, text):
        self.text = text

    def get_json_dict(self):
        # pinpointing the exact location of the json dictionary containing the picture ids
        start_index = self.text.find(self.js_variable)
        start_index = start_index + len(self.js_variable) - 1
        end_index = self.text.find(';', start_index)
        actress_json_data_string = self.text[start_index:end_index]
        return json.loads(actress_json_data_string)


# LinkBuilder class needs a model name to be instantiated, which is then used
# to build the link to the actual picture
class LinkBuilder:

    def __init__(self, model):
        self.model = model.replace('_', '-')

    def set_model(self, model):
        self.model = model.replace('_', '-')

    def build_link(self, pid):
        return "https://pics.wikifeet.com/" + self.model + "-Feet-" + str(pid) + ".jpg"


# JPGDownloader class can download a picture from any given link to a specified path
class JPGDownloader:

    def __init__(self, path):
        self.path = path

    def download_image(self, link):
        filename = link.split('/')[-1]
        filepath = os.path.join(self.path, filename)
        r = requests.get(link, non_bot_header, stream=True)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
        else:
            print("Error: {}".format(r.status_code))


# pid = picture id, used later to build a link to the picture itself
def build_pid_list(json_dict):
    pids = []
    for index, element in enumerate(json_dict):
        pids.append(json_dict[index]['pid'])
    pids.sort()

    return pids


if __name__=="__main__":
    try:

        # obtaining arguments from command line 
        parser = argparse.ArgumentParser()

        parser.add_argument("--url")
        parser.add_argument("--download_path") #might remove. not needed with download manager setup the current way

        args = parser.parse_args()
        
        hmrw = Path(abspath(getsourcefile(lambda:0))).parents[0]
        urlpath = os.path.join(hmrw , "urls")
            
        urlizt = open(urlpath, 'r')
        ulrz = urlizt.readlines()
        urlizt.close()

        
        if len(sys.argv) != 1:
            url = args.url
            # get model name from the link ending
            model_name = url.split('/')[-1]

            # if link looks like a wikifeet.com or wikifeetx.com one, proceed
            if re.search(wikifeet_pattern, url) or re.search(wikifeetx_pattern, url):
                r = requests.get(url, non_bot_header)

                # checking if the link is actually valid, and if we can obtain (GET) the page
                if r.status_code == 200:
                    if (url + "\n") not in ulrz:
                        urlizt1 = open(urlpath, 'a+') #adds the url to the bulk download list
                        urlizt1.write(url + "\n")
                        urlizt1.close()
                        print("link added to list")
                    else:
                        print("link already in list")
                else:
                    print("Error: {}".format(r.status_code))
            else:
                print("Error: No wikifeet.com url detected")
        else:
            print()
            
            
            
            
            
            
        if len(sys.argv) == 1:
			#abspath(getsourcefile(lambda:0)) 
        
            for urlz in ulrz:
                url = urlz.strip()
                
                model_name = url.split('/')[-1]
                moddow = os.path.join(hmrw, model_name)
                favsfold = os.path.join(moddow, "favs")
                oldsfold = os.path.join(moddow, "old")


                print('\n' "" +  model_name + " is next")
                
                if re.search(wikifeet_pattern, url) or re.search(wikifeetx_pattern, url):
                    r = requests.get(url, non_bot_header)

                # checking if the link is actually valid, and if we can obtain (GET) the page
                    if r.status_code == 200:

                        # begin extracting procedure on downloaded page
                        json_extractor = JSONExtractor(r.text)
                        extracted_json = json_extractor.get_json_dict()

                        pids = build_pid_list(extracted_json)
                        link_builder = LinkBuilder(model_name)

                        # deciding where to put downloaded pictures
                        if os.path.exists(moddow):
                            download_path = moddow
                            for filsss in os.listdir(moddow):
                                if filsss.endswith(".jpg"):
                                #if os.path.isfile(filsss):
                                    if not os.path.exists(oldsfold):
                                        os.mkdir(oldsfold)
                                    if not os.path.exists(favsfold):
                                        os.mkdir(favsfold )
                                    filsrc = os.path.join(moddow, filsss)
                                    fildest = os.path.join(oldsfold, filsss)
                                    shutil.move(filsrc, fildest)
                                    #print('Moved:', filsss)
									
                            
                        else:
                            print("Path does not exist, it will be created")
                            os.mkdir(moddow)
                            download_path = moddow
                            print(moddow)

                            os.mkdir(favsfold)
                            os.mkdir(oldsfold)


                        # now we're ready to go
                        download_pid_path = os.path.join(download_path, model_name)                
                        jpgdownloader = JPGDownloader(download_path)
    
                        # download every picture by building the link with a pid first, 
                        # then feeding it to the JPGDownloader object "download_image" method;
                        # progress is expressed in % points
                        for index, pid in enumerate(pids):
                            link = link_builder.build_link(pid)
                            if not os.path.isfile(download_pid_path):
                                os.mknod(download_pid_path)
                            if (str(pid) + " " not in (open(download_pid_path).read())): # if already downloaded dont otherwise do
                                jpgdownloader.download_image(link)
                                dwnpid = open(download_pid_path, 'a+')
                                dwnpid.write(str(pid) + " \n")
                                dwnpid.close()
                                wrotesmthing = 1 # flags for later printing
                                #print("  downloading PID " + str(pid) + " ")
                                print()
                            else:
                                #print('\r' " " + str(pid) + " already in list ")
                                wrotesmthing = 0
                                #print()
                            if wrotesmthing == 1: # progress bar
                                print('\r' " Progress: {:.1f}%".format(((index + 1) / len(pids))*100), model_name + " is downloading. currently picture " + str(pid) , end='') 
                            else:
                                print(" Progress: {:.1f}%".format(((index + 1) / len(pids))*100), end='\r')
                    else:
                        print("Error: {}".format(r.status_code))
                else:
                    print("Error: No wikifeet.com url detected")

        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
    sys.exit(0)


""" 
useful examples during editting
  abspath(getsourcefile(lambda:0)) #supposed to locate the current py file
        
if a special character is in the url such as with pokimanes then you have to find the text version like ' = %27


""" #"""
