# python-wikifeet-downloader

Simple tool to download all pictures from a model page on www.wikifeet.com or www.wikifeetx.com 
Simply place the urls of the pages you wish to download one per line into a text file named "urls" in the folder with the script and it will download them in order




## Terminal Input Usage (likely to have been broken during editting but kept for documenting reasons from the original)

```text
wikifeet_downloader.py [-h] [--download_path DOWNLOAD_PATH] url
```

Immediate command to download all pictures:

```text
wikifeet_downloader.py url
```

If no download path is specified, the tool defaults to creating a folder in the current directory with the model's name.
