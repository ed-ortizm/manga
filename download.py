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
dap_files = parser.get('files', 'dap')
# extension = parser.get('files', 'extension')
server = parser.get('parameters', 'server')
sas_directory = parser.get('directories', 'server')
mpl = parser.get('parameters', 'version')
output_directory = parser.get('directories', 'output')

subprocess.call([
    'rsync', flag, '--progress',
    '--password-file', password_file,
    '--include', '"*/"',
    '--include', f'"{dap_files}"',
    '--exclude', '"*"',
    f'rsync://{server}/{sas_directory}/{mpl}/{product}/',
    output_directory
])
