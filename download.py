#! /usr/bin/env python3
####################################################################
from configparser import ConfigParser, ExtendedInterpolation
import subprocess

###############################################################################
parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read("download.ini")
###############################################################################
flag = parser.get("parameters", "flag")
password_file = parser.get("files", "password")
product = parser.get("files", "product")
dap_files = parser.get("files", "dap")
server = parser.get("parameters", "server")
sas_directory = parser.get("directories", "server")
mpl = parser.get("parameters", "version")
output_directory = parser.get("directories", "output")

subprocess.call(
    [
        "rsync",
#        "--dry-run",
        flag,
        "--progress",
        "--password-file",
        password_file,
        "--exclude",
        "*qa",
        "--exclude",
        "*ref",
        "--include",
        '"*/"',
        "--include",
        f'{dap_files}',
        "--exclude",
        '"*"',
        f"rsync://{server}/{sas_directory}/{mpl}/{product}/",
        output_directory,
    ]
)
# rsync -ahLrvz --progress --password-file /home/edgar/pass.pss --include "*/" --include "manga-*-*-*-HYB10-MILESHC-MASTARHC2.fits.gz" --exclude "*" rsync://sdss@dtn01.sdss.utah.edu/sas/mangawork/manga/spectro/analysis/MPL-11/HYB10-MILESHC-MASTARHC2/ /home/edgar/oso/data/manga/analysis
