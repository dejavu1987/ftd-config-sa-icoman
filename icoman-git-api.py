import base64
import re
import time
from zipfile import ZipFile
import requests
from dotenv import load_dotenv
import os
import pyvips
import numpy
from PIL import Image

load_dotenv()

# Define the URL and icons directory
icon_repo_base = os.getenv('ICON_REPO_BASE')
icons_dir = "icons"  # Change this to your desired icons directory
delay_seconds = 1

# List of icon names
icon_names = [
    "volume-minus",
    "skip-next",
    "play-pause",
    "skip-previous",
    "volume-off",
    "access-point",
    "access-point-off",
    "record-rec",
    "stop",
    "thumb-up",
    "thumb-down",
    "youtube-subscription",
    "share",
    "content-cut",
    "content-copy",
    "content-paste",
    "undo",
    "tab-plus",
    "tab-remove",
    "refresh",
    "bookmark",
    "layers",
    "crop",
    "image-filter-black-white",
    "undo",
    "border-none-variant"
]

# Access the GITHUB_TOKEN from the environment
github_token = os.getenv("GITHUB_TOKEN")

# Define the headers with the token
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {github_token}",
}

# Create the icons directory if it doesn't exist
os.makedirs(icons_dir, exist_ok=True)

# Empty icons directory
file_list = os.listdir(icons_dir)
for file in file_list:
    file_path = os.path.join(icons_dir, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Download icons and save to the icons directory
for icon_name in icon_names:
    icon_repo = f"{icon_repo_base}{icon_name}.svg"
    response = requests.get(icon_repo, headers=headers)
    print(response.content)
    if response.status_code == 200:
        data = response.json()
        base64_content = data["content"]
        content_bytes = base64.b64decode(base64_content)
        # Hacky way to resize the svg
        width = 75
        height = 75
        svg = re.sub(
                r'(viewBox="[^"]+")', f'\\1 width="{width}" height="{height}"', content_bytes.decode('utf-8')
            )
        
        png = pyvips.Image.new_from_buffer(svg.encode('utf-8'),"")

        # turn black and white
        rgba = numpy.array(png)
        rgba[rgba[..., -1] != 0] = [255, 255, 255, 255]
        rgba[rgba[..., -1] == 0] = [0, 0, 0, 255]

        bmp = Image.fromarray(rgba).convert(mode='RGB', colors=24)
        bmp.save(os.path.join(icons_dir, f'{icon_name}.bmp'), 'BMP')
        print(f"Saved {icon_name}.bmp\n")

    else:
        print(f"Failed to download {icon_name}.svg\n")
        # Print response headers
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")

        # Print response content (if available)
        if response.content:
            print("Response Content:")
            print(response.content)
    # Trying adding delays for 404 errors
    time.sleep(delay_seconds)
print("Icons ready.\n")

# Create a ZipFile object in write mode
with ZipFile("icons.zip", 'w') as zipf:
    # Walk through the directory and add files to the zip
    for foldername, subfolders, filenames in os.walk(icons_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # Define the name of the file inside the zip
            archive_name = os.path.relpath(file_path, icons_dir)
            zipf.write(file_path, archive_name)

print(f"Zip ready\n")