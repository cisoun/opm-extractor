"""
Files extractor for OPM archives (OTRS package).

Author: Cyriaque 'cisoun' Skrapits
"""


import argparse
import base64
import os
from xml.dom import minidom


def parse():
    parser = argparse.ArgumentParser(
        description='Extract files from an OPM file into a new directory.')
    parser.add_argument(
        'file',
        type=str,
        help='OPM file to extract'
    )
    return parser.parse_args()


def extract(path):
    folder = os.path.splitext(path)[0]  # Remove extension (.opm).

    opm = minidom.parse(path)
    file_list = opm.getElementsByTagName('Filelist')
    files = file_list.item(0).getElementsByTagName('File')

    # Extract files.
    for file in files:
        file_path = folder + '/' + file.getAttribute('Location')
        file_root = os.path.dirname(file_path)

        print('Extracting %s' % file_path)

        # Recreate file's directory.
        os.makedirs(file_root, exist_ok=True)

        # Recreate file.
        with open(file_path, 'wb+') as f:
            data = file.firstChild.data
            f.write(base64.b64decode(data))


def main():
    args = parse()
    extract(args.file)


main()
