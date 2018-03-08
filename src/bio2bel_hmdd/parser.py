# -*- coding: utf-8 -*-

import logging
import os
from urllib.request import urlretrieve

from .constants import DATA_FILE_PATH, DATA_URL

log = logging.getLogger(__name__)


def download_hmdd(force_download=False):
    """Download the HMDD database as a TSV

    :param bool force_download: If true, forces the data to get downloaded again; defaults to False
    :return: The system file path of the downloaded file
    :rtype: str
    """
    if os.path.exists(DATA_FILE_PATH) and not force_download:
        log.info('using cached data at %s', DATA_FILE_PATH)
    else:
        log.info('downloading %s to %s', DATA_URL, DATA_FILE_PATH)
        urlretrieve(DATA_URL, DATA_FILE_PATH)

    return DATA_FILE_PATH
