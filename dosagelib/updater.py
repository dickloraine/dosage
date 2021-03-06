# -*- coding: iso-8859-1 -*-
"""
Function to check for updates.
"""
import os
import dosagelib
from dosagelib import configuration
from .util import urlopen
from distutils.version import StrictVersion
import requests


UPDATE_URL = "https://api.github.com/repos/webcomics/dosage/releases/latest"

def check_update ():
    """Return the following values:
       (False, errmsg) - online version could not be determined
       (True, None) - user has newest version
       (True, (version, url string)) - update available
       (True, (version, None)) - current version is newer than online version
    """
    version, value = get_online_version()
    if version is None:
        # value is an error message
        return False, value
    if version == dosagelib.__version__:
        # user has newest version
        return True, None
    if is_newer_version(version):
        # value is an URL linking to the update package
        return True, (version, value)
    # user is running a local or development version
    return True, (version, None)


def get_online_version ():
    """Download update info and parse it."""
    session = requests.session()
    page = urlopen(UPDATE_URL, session).json()
    version, url = None, None
    version = page['tag_name']

    if os.name == 'nt':
        url = next((x['browser_download_url'] for x in page['assets'] if x['content_type'] == 'application/x-msdos-program'), configuration.Url)
    else:
        url = page['tarball_url']
    return version, url


def is_newer_version (version):
    """Check if given version is newer than current version."""
    return StrictVersion(version) > StrictVersion(dosagelib.__version__)
