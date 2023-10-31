import concurrent.futures
from io import BytesIO
from dotenv import load_dotenv
import numpy
import os
import pyvips
from pathlib import Path
from PIL import Image
import re
import requests
import shutil
import time
from zipfile import ZipFile

load_dotenv()
global_start_time = time.time()
# Define the URL and icons directory
icon_repo_base = os.getenv('ICON_REPO_RAW_BASE')
icons_dir = "icons"  # Change this to your desired icons directory
icons_cache_dir = ".icons-cache"  # Change this to your desired icons cache directory
icons_source_dir = "icons-source"  # Change this to your desired icons source directory
delay_seconds = 0

# List of icon names
# Get it from https://ftd.anilmaharjan.com.np/
icon_names = [
    "volume-plus",
    "volume-minus",
    "skip-next",
    # ...
]

def prepare_dirs():
    # Create the icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    os.makedirs(icons_cache_dir, exist_ok=True)

    # Empty icons directory
    file_list = os.listdir(icons_dir)
    for file in file_list:
        file_path = os.path.join(icons_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def resize_svg(svgInput):
    # Hacky way to resize the svg
    width = 75
    height = 75
    return re.sub(
            r'(viewBox="[^"]+")', f'\\1 width="{width}" height="{height}"', svgInput
        )

def make_bmp(png):
     # turn black and white
    rgba = numpy.array(png)
    rgba[rgba[..., -1] != 0] = [255, 255, 255, 255]
    rgba[rgba[..., -1] == 0] = [0, 0, 0, 255]

    bmp = Image.fromarray(rgba).convert(mode='RGB', colors=24)
    return bmp


def time_taken(start_time, end_time):
    elapsed_time = end_time - start_time

    if elapsed_time >= 1:
        color = '\33[31m'  # Red color for times >= 1s
        unit = "s"
    elif elapsed_time >= 0.001:
        color = '\33[33m'  # Orange color for times between 1ms and 1s
        elapsed_time *= 1000  # Convert to milliseconds
        unit = "ms"
    else:
        color = '\33[32m'  # Green color for times < 1ms
        elapsed_time *= 1000000  # Convert to microseconds
        unit = "µs"
    
    reset_color = '\33[0m'  # Reset color to default

    time_string = f"Time taken: {color}{elapsed_time:.2f} {unit}{reset_color}"
    print(time_string
          )
def process_icon(icon_name):
    start_time = time.time()
    cached_icon = Path(os.path.join(icons_cache_dir, f'{icon_name}.bmp'))
    if cached_icon.is_file():
        print(f"Cached found {icon_name}.bmp")
        shutil.copy(cached_icon, os.path.join(icons_dir, f'{icon_name}.bmp'))
    else:
        icon_repo_url = f"{icon_repo_base}{icon_name}.svg"
        response = requests.get(icon_repo_url)

        if response.status_code == 200:
            svg = resize_svg(response.content.decode('utf-8'))
            icon_buff = svg.encode('utf-8')
            
            png = pyvips.Image.new_from_buffer(icon_buff, "")

            bmp = make_bmp(png)

            bmp.save(os.path.join(icons_dir, f'{icon_name}.bmp'), 'BMP')
            bmp.save(os.path.join(icons_cache_dir, f'{icon_name}.bmp'), 'BMP')
            print(f"Saved {icon_name}.bmp")

        else:
            print(f"Failed to download {icon_name}.svg")

    end_time = time.time()
    time_taken(start_time, end_time)

def generate_icons(icon_names):
    prepare_dirs()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_icon, icon_names)
    print("Icons ready.")

def generate_and_zip_icons(icon_names):
    generate_icons(icon_names)
    # Create a ZipFile object in write mode
    with ZipFile("icons.zip", 'w') as zipf:
        # Walk through the directory and add files to the zip
        for foldername, _, filenames in os.walk(icons_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Define the name of the file inside the zip
                archive_name = os.path.relpath(file_path, icons_dir)
                zipf.write(file_path, archive_name)

    print(f"Zip ready")
    shutil.rmtree(icons_dir)

def get_zip_buffer(icon_names):
    generate_icons(icon_names)
    output_buffer = BytesIO()
    with ZipFile(output_buffer, 'w') as zipf:
        for foldername, _, filenames in os.walk(icons_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                archive_name = os.path.relpath(file_path, icons_dir)
                zipf.write(file_path, archive_name)
    shutil.rmtree(icons_dir)
    return output_buffer.getvalue()

global_end_time = time.time()
time_taken(global_start_time, global_end_time)