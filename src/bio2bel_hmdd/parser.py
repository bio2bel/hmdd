# -*- coding: utf-8 -*-

"""Downloaders for Bio2BEL HMDD"""

from bio2bel.downloading import make_df_getter
from .constants import HMDD_COLUMNS, HMDD_PATH, HMDD_URL

__all__ = ['get_hmdd_df']

get_hmdd_df = make_df_getter(
    HMDD_URL,
    HMDD_PATH,
    sep='\t',
)
"""Loads the HMDD into a data frame

    1) Index
    2) miRNA ID
    3) MeSHDisease term
    4) PubMed ID
    5) Description
"""
