#! /usr/bin/env python3
####################################################################
from configparser import ConfigParser, ExtendedInterpolation
import subprocess
################################################################################
parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read('download.ini')
################################################################################
flag = parser.get('parameters', 'flag')
password_file = parser.get('files', 'password')
product = parser.get('files', 'product')
extension = parser.get('files', 'extension')
server = parser.get('parameters', 'server')
server_location = parser.get('directories', 'server')
mpl = parser.get('parameters', 'version')
output_directory = parser.get('directories', 'output')

subprocess.call([
    'rsync', flag, '--progress',
    '--password-file', password_file,
    '--include', '"*/"',
    '--include', f'manga-*-*-*-{product}.{extension}',
    '--exclude', '"*"',
    f'rsync:{server}/{server_location}/{mpl}/{product}/',
    output_directory
])
