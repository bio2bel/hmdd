# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MiRNA(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Disease(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Association(Base):
    id = Column(Integer, primary_key=True)
    pubmed = Column(String(32), nullable=False)
    description = Column(String)
    mirna_id = Column(Integer, ForeignKey('mirna.id'))
    mirna = relationship(MiRNA)
    disease_id = Column(Integer, ForeignKey('disease.id'))
    disease = relationship(Disease)
