import subprocess
import urllib.request
import os
import zipfile
import glob
import argparse
import requests


def download(thing_number):
    thing_link = f"https://www.thingiverse.com/thing:{thing_number}/zip"

    r = requests.get(thing_link)
    download_link = r.url
    filename = download_link.rsplit('/', 1)[1]

    zippath = os.path.join(SAVE_PATH, filename)

    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(download_link, zippath)

    filepath = zippath.rstrip(".zip")

    print(f"Extracting {filename}...")
    zipfile.ZipFile(zippath, "r").extractall(filepath)

    os.remove(zippath)

    return filepath, filename


def find_stls(path, filename):
    file_list = []
    if os.path.exists(os.path.join(path, "files")):
        path = os.path.join(path, "files")

    elif os.path.exists(os.path.join(path, filename.rstrip(".zip"))):
        path = os.path.join(path, filename.rstrip(".zip"))

    for filepath in glob.glob(os.path.join(path, "*.stl")):
        file_list.append('"' + filepath + '"')

    return file_list


parser = argparse.ArgumentParser(
    description='Downloads, extracts, and opens STL files from thingiverse')
parser.add_argument('thing_number', type=int,
                    help='Thing number from Thingiverse')
parser.add_argument(
    '-m', '--mass', help='Whether or not to save to mass production files', action="store_true")
parser.add_argument(
    '--no-cura', help='Specify to not open cura after downloading files', action="store_true")
args = parser.parse_args()

if args.mass == True:
    SAVE_PATH = "F:/3D Prints/Mass production"

else:
    SAVE_PATH = "F:/3D Prints/In progress or not printed"

filepath, filename = download(args.thing_number)

if args.no_cura == False:
    stls = find_stls(filepath, filename)
    stl_list = ' '.join(stls)
    print("Starting Cura...")
    os.system('cura ' + stl_list)
