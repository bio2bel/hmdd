# -*- coding: utf-8 -*-

"""Constants for Bio2BEL HMDD."""

import os

from bio2bel.utils import get_data_dir

VERSION = '0.0.3-dev'


def get_version() -> str:
    """Get the current software version of Bio2BEL HMDD."""
    return VERSION


MODULE_NAME = "hmdd"
DATA_DIR = get_data_dir(MODULE_NAME)

HMDD_URL = "http://www.cuilab.cn/static/hmdd3/data/alldata.txt"
HMDD_PATH = os.path.join(DATA_DIR, "alldata.txt")
HMDD_COLUMNS = [
    'category',
    'mir',
    'disease',
    'pmid',
    'root_name',
    'doid',
    'icd10cm',
    'mesh',
    'omim',
    'hpo',
    'description',
]
