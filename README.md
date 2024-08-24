# BoxVideoDownloader

This script is a video downloader for Box（https://app.box.com/）.

I have only tested this script on Windows 10/11, so I am not sure if it will work on other operating systems.

I used Python 3.10.9.

## Usage
## 1. Download and install ffmpeg via the following URL, if you don't already have it:
https://www.ffmpeg.org/download.html

This link might be useful: https://phoenixnap.com/kb/ffmpeg-windows

## 2. Access the Box URL for the video you want to download.

## 3. Open the browser's Developer Console and click the Network tab.
You may need to reload the page if nothing appears in the Network tab.

## 4. Search for `.mpd` to find the `manifest.mpd` link, which should look like the one in the photo.

Copy the MPD link.

![boxmpd](https://github.com/user-attachments/assets/d2b77aa6-38bf-499a-be8b-54b4a8c4bebf)

## 5. Open `cmd.exe` and execute the following command:

```
python boxvideodownloader.py [mpd link]
```

A video folder and an audio folder will be created automatically, and the `.m4s` files will be downloaded into these folders. Please wait until the download is complete.

## 6. When the download is finished, ffmpeg will merge the files and create a `downloaded.mp4` file.
The .m4s files will be automatically deleted too.
