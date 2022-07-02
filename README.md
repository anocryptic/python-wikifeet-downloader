# python-wikifeet-downloader

Simple tool to download all pictures from a model page on www.wikifeet.com or www.wikifeetx.com 

Simply place the urls of the pages you wish to download one per line into a text file named "urls" in the folder with the script and it will download them in order. 

the downloader will make a folder directory when run where it will download pictures to. it will also move any files in the model folders into an old files folder for ease of use identifying which pictures are the newest downloads without needing to browse the actual download list output. the downloader will also create a favorites folder which the user can drop pictures into which wont be moved to the old folder on next run

to quickly add a url to the end of the list when running the downloader run "python3 wikifeet_downloader.py --url link2add" where link2add is replaced with the link to the wikifeet page you wish to download. if the link is already added it will notify you

----trouble shooting----
if a file downloads wrong and you need to redownload them - In the models folder delete the picture id from the txt file and it will redownload next run
if a models page has a special character in the link it can be helpful to find the html character number codes such as on this page https://www.whatsmyip.org/html-characters/
