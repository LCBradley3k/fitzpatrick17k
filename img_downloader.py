#
# This file is meant to run before train.py.
# It loads the fitzpatrick17k.csv into a pandas dataframe.
# From each image URL, it downloads them to a target directory.
#

import pandas as pd
import requests
import os
import hashlib

DBG = False

#
# Read CSV file into a Pandas dataframe
#
df = pd.read_csv('fitzpatrick17k.csv')

#
# Define the directory to save the images
#
save_dir = "images"

#
# Create the directory if it doesn't exist
#
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

#
# Define the headers to specify the image format.
# Web server seems to require any random user-agent, hence "XY"
#
headers = {
    'User-Agent': 'XY',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

#
# Loop through the URLs and download the images
#
i = 0
for url in df['url']:
    if isinstance(url, str):
        try:

            print("downloading... ", i, url)
            filename = os.path.join(save_dir, url.split('/')[-1])

            #
            # Additional split required for URLs from http://atlasdermatologico.com 
            # because they are of form "img?imageId=5630", and we only the ID at the end.
            #
            if "atlasdermatologico" in url:
                filename = os.path.join(save_dir, filename.split('=')[-1])
                filename = filename + ".jpg"

        except Exception as e:
            print(f'Error splitting URL {url}: {e}')

        response = requests.get(url, headers=headers)

        if DBG:
            print("response: ", response.status_code)
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        with open(filename, 'rb') as f:
            file_contents = f.read()

        # Get the MD5 hash of the file contents
        md5_hash = hashlib.md5(file_contents).hexdigest()
        new_filename = os.path.join(save_dir, md5_hash)
        os.rename(filename, new_filename)
    else:
        print("no URL in entry ", i, url)

    #
    # Increment i to keep track of unique entries.
    #
    i = i + 1

# end loop