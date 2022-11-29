import argparse
import glob
import io
import os
import re
import subprocess
import zipfile

import requests

SAVE_PATH = ""

def _download(thing_number, section):
    thing_link = f"https://cdn.thingiverse.com/tv-zip/{thing_number}"

    r = requests.get(thing_link, allow_redirects=True, timeout=30)
    assert r.ok, "Failed to download thing"
    filename = re.findall('filename="(.+)\.zip"', r.headers.get('content-disposition'))[0]

    if section is not None:
        save_path = os.path.join(SAVE_PATH, section)
    else:
        save_path = SAVE_PATH

    print(f"Downloading {filename}...")
    filepath = os.path.join(save_path, filename)

    print(f"Extracting {filename}...")
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(filepath)

    return filepath, filename


def _find_stls(path, file):
    if os.path.exists(os.path.join(path, "files")):
        path = os.path.join(path, "files")

    elif os.path.exists(os.path.join(path, file)):
        path = os.path.join(path, file)

    file_list = [f'"{path}"' for path in glob.glob(os.path.join(path, "*.stl"))]

    return file_list


parser = argparse.ArgumentParser(description='Downloads, extracts, and opens STL files from thingiverse')
parser.add_argument('thing_number', type=int, metavar='N', help='Thing number from Thingiverse')
parser.add_argument('--section', '-s', type=str, default=None, help='Section to put files in')
parser.add_argument('--no-cura', help='Specify to not open cura after downloading files', action="store_true")
args = parser.parse_args()

path, file = _download(args.thing_number, args.section)

if not args.no_cura:
    stls = _find_stls(path, file)
    COMMAND = 'ultimaker-cura ' + ' '.join(stls)
    print("Starting Cura...")
    subprocess.Popen(COMMAND)
