# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from pybel.constants import ASSOCIATION
from pybel.dsl import mirna as mirna_dsl, pathology as pathology_dsl
from .constants import MODULE_NAME

MIRNA_TABLE_NAME = '{}_mirna'.format(MODULE_NAME)
DISEASE_TABLE_NAME = '{}_disease'.format(MODULE_NAME)
ASSOCICATION_TABLE_NAME = '{}_association'.format(MODULE_NAME)

Base = declarative_base()


class MiRNA(Base):
    """This class represents the miRNA table"""

    __tablename__ = MIRNA_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False, unique=True, index=True, doc='name from mirBase')

    def __repr__(self):
        return self.name

    def to_bel(self):
        return mirna_dsl(namespace='MIRBASE', name=str(self.name))


class Disease(Base):
    """This class represents the disease table"""

    __tablename__ = DISEASE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False, unique=True, index=True, doc='name from MeSH')

    def __repr__(self):
        return self.name

    def to_bel(self):
        return pathology_dsl(namespace='MESH', name=str(self.name))


class Association(Base):
    """This class represents the miRNA disease association table"""

    __tablename__ = ASSOCICATION_TABLE_NAME

    id = Column(Integer, primary_key=True)

    pubmed = Column(String(32), nullable=False)
    description = Column(Text, doc='This is a manually curated association')

    mirna_id = Column(Integer, ForeignKey('{}.id'.format(MIRNA_TABLE_NAME)))
    mirna = relationship('MiRNA')

    disease_id = Column(Integer, ForeignKey('{}.id'.format(DISEASE_TABLE_NAME)))
    disease = relationship('Disease')

    def add_to_bel_graph(self, graph):
        """Add this association to a BEL graph

        :param pybel.BELGraph graph:
        :rtype: str
        """
        return graph.add_qualified_edge(
            self.mirna.to_bel(),
            self.disease.to_bel(),
            relation=ASSOCIATION,
            citation=str(self.pubmed),
            evidence=str(self.description),
        )

    def __repr__(self):
        return '{} and {} from {}'.format(self.mirna, self.disease, self.pubmed)
