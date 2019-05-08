"""
Files extractor for OPM archives (OTRS package).

Author: Cyriaque 'cisoun' Skrapits
"""


import argparse
import base64
from xml.dom import minidom


def parse():
    parser = argparse.ArgumentParser(description='Extract files from an OPM file.')
    parser.add_argument(
        'file',
        type=str,
        help='OPM file to extract'
    )
    return parser.parse_args()


def extract(path):
    opm = minidom.parse(path)
    file_list = opm.getElementsByTagName('Filelist')
    files = file_list.item(0).getElementsByTagName('File')

    for file in files:
        location = file.getAttribute('Location')
        name = location.replace('/', '.')
        data = file.firstChild.data

        print('Extracting %s' % name)

        with open(name, 'wb+') as f:
            f.write(base64.b64decode(data))


def main():
    args = parse()
    extract(args.file)


main()
