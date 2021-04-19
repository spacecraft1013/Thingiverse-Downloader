import urllib.request
import os
import zipfile
import glob
import argparse
import requests
import subprocess


def _download(thing_number):
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


def _find_stls(path, filename):
    if os.path.exists(os.path.join(path, "files")):
        path = os.path.join(path, "files")

    elif os.path.exists(os.path.join(path, filename.rstrip(".zip"))):
        path = os.path.join(path, filename.rstrip(".zip"))

    file_list = [f'"{path}"' for path in glob.glob(os.path.join(path, "*.stl"))]

    return file_list


parser = argparse.ArgumentParser(description='Downloads, extracts, and opens STL files from thingiverse')
parser.add_argument('thing_numbers', nargs='+', metavar='N', help='Thing numbers from Thingiverse')
parser.add_argument('-s', '--section', type=str, metavar='S', help='What subfolder to download the file to', required=False)
parser.add_argument('-m', '--mass', help='Whether or not to save to mass production files', action="store_true")
parser.add_argument('--no-cura', help='Specify to not open cura after downloading files', action="store_true")
args = parser.parse_args()

if args.mass:
    SAVE_PATH = "F:/3D Prints/Mass production"

elif args.section:
    SAVE_PATH = f"F:/3D Prints/In progress or not printed/{args.section}"
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

else:
    SAVE_PATH = "F:/3D Prints/In progress or not printed"

for thing_number in args.thing_numbers:
    filepath, filename = _download(thing_number)

    if not args.no_cura:
        stls = _find_stls(filepath, filename)
        command = 'cura ' + ' '.join(stls)
        print("Starting Cura...")
        subprocess.Popen(command)
