import os
import sys
import requests
import subprocess
import glob
import time
from urllib.parse import urlparse, parse_qs, urlunparse
import xml.etree.ElementTree as ET
import argparse

headers = {
    "authority": "public.boxcloud.com",
    "accept": "*/*",
    "accept-language": "ja;q=0.5",
    "origin": "https://app.box.com",
    "referer": "https://app.box.com/",
    "sec-ch-ua": '"Brave";v="114", "Chromium";v="114", "Not-A.Brand";v="8"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

parser = argparse.ArgumentParser(description='プログラムの説明')

parser.add_argument('url', help='URL')

parser.add_argument('-i', '--index', help='どのファイルからダウンロードを始めるか')

try:
    args = parser.parse_args()
    url = args.url
    if args.index:
        i = int(args.index)
    else:
        i = 1
except argparse.ArgumentError as e:
    print("Usage: python script.py <url>")

os.makedirs('video/1080', exist_ok=True)
os.makedirs('audio/0', exist_ok=True)

response = requests.get(url, headers=headers)
content = response.content

root = ET.fromstring(content)
for adaptation_set in root.findall(".//AdaptationSet[@contentType='video']"):
    for representation in adaptation_set.findall("Representation"):
        if representation.get('codecs') == 'avc1.42c028':
            adaptation_set.remove(representation)

new_xml_data = ET.tostring(root, encoding='utf-8').decode('utf-8')

with open('manifest.mpd', 'w') as f:
    f.write(new_xml_data)

parsed_url = urlparse(url)
params = parse_qs(parsed_url.query)

new_path = parsed_url.path.rsplit('/', 1)[0] + '/video/1080/init.m4s'
new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
response = requests.get(new_url, headers=headers)
content_init = response.content
with open('video/1080/init.m4s', 'wb') as f:
    f.write(content_init)

new_path = parsed_url.path.rsplit('/', 1)[0] + '/audio/0/init.m4s'
new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
response = requests.get(new_url, headers=headers)
content_init = response.content
with open('audio/0/init.m4s', 'wb') as f:
    f.write(content_init)

print("DL START!!")

try:
    while True:
        new_path = parsed_url.path.rsplit('/', 1)[0] + '/video/1080/' + str(i) + '.m4s'
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        response = requests.get(new_url, headers=headers)
        time.sleep(0.1)
        if response.status_code == 200:
            content_i = response.content
            with open(f'video/1080/{i}.m4s', 'wb') as f:
                f.write(content_i)
            if i % 100 == 0:
                print(f'Downloaded video file {i}')
        elif response.status_code == 503:
            time.sleep(1)
            content_i = response.content
            with open(f'video/1080/{i}.m4s', 'wb') as f:
                f.write(content_i)
            if i % 100 == 0:
                print(f'Downloaded video file {i}')
        else:
            break

        new_path = parsed_url.path.rsplit('/', 1)[0] + '/audio/0/' + str(i) + '.m4s'
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        response = requests.get(new_url, headers=headers)
        time.sleep(0.1)
        if response.status_code == 200:
            content_i = response.content
            with open(f'audio/0/{i}.m4s', 'wb') as f:
                f.write(content_i)
            if i % 100 == 0:
                print(f'Downloaded audio file {i}')
        elif response.status_code == 503:
            time.sleep(1)
            content_i = response.content
            with open(f'audio/0/{i}.m4s', 'wb') as f:
                f.write(content_i)
            if i % 100 == 0:
                print(f'Downloaded audio file {i}')
        else:
            break

        i += 1
except:
    print(e)
    print("\007")
    
subprocess.run(['ffmpeg', '-i', 'manifest.mpd', '-codec', 'copy', 'downloaded.mp4'])

# when merged, delete files.
os.remove('manifest.mpd')
for file in glob.glob('video/1080/*.m4s'):
    os.remove(file)
for file in glob.glob('audio/0/*.m4s'):
    os.remove(file)
    
print("\007")