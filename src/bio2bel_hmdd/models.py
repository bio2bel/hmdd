# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .constants import  MODULE_NAME

MIRNA_TABLE_NAME = '{}_mirna'.format(MODULE_NAME)
DISEASE_TABLE_NAME = '{}_disease'.format(MODULE_NAME)
ASSOCICATION_TABLE_NAME = '{}_association'.format(MODULE_NAME)

Base = declarative_base()


class MiRNA(Base):
    """This class represents the miRNA table"""

    __tablename__ = MIRNA_TABLE_NAME
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False,doc='name from mirBase')


class Disease(Base):
    """This class represents the disease table"""

    __tablename__ = DISEASE_TABLE_NAME
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False,doc='name from MeSH')


class Association(Base):
    """This class represents the miRNA disease association table"""

    __tablename__ = ASSOCICATION_TABLE_NAME
    id = Column(Integer, primary_key=True)
    pubmed = Column(String(32), nullable=False)
    description = Column(String,doc='This is a manually curated association')
    mirna_id = Column(Integer, ForeignKey('{}.id'.format(MIRNA_TABLE_NAME)))
    mirna = relationship(MiRNA)
    disease_id = Column(Integer, ForeignKey('{}.id'.format(ASSOCICATION_TABLE_NAME)))
    disease = relationship(Disease)
