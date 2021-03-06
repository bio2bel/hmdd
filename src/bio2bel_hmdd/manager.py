# -*- coding: utf-8 -*-

"""Manager for Bio2BEL HMDD."""

import logging
from typing import List, Mapping, Optional

from tqdm import tqdm

import bio2bel_mesh
import bio2bel_mirbase
from bio2bel import AbstractManager
from bio2bel.manager.bel_manager import BELManagerMixin
from bio2bel.manager.flask_manager import FlaskMixin
from pybel import BELGraph
from .constants import MODULE_NAME
from .models import Association, Base, Disease, MiRNA
from .parser import get_hmdd_df

__all__ = ['Manager']

log = logging.getLogger(__name__)


class Manager(AbstractManager, BELManagerMixin, FlaskMixin):
    """Bio2BEL Manager for HMDD."""

    module_name = MODULE_NAME
    flask_admin_models = [MiRNA, Disease, Association]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name_mirna = {}
        self.name_disease = {}

    @property
    def _base(self):
        return Base

    def is_populated(self) -> bool:
        """Check if the database is already populated."""
        return 0 < self.count_associations()

    def get_mirna_by_name(self, name: str) -> Optional[MiRNA]:
        """Gets an miRNA from the database if it exists

        :param name: A mirBase name
        """
        return self.session.query(MiRNA).filter(MiRNA.name == name).one_or_none()

    def get_disease_by_name(self, name: str) -> Optional[Disease]:
        """Gets a Disease from the database if it exists

        :param name: A MeSH disease name
        """
        return self.session.query(Disease).filter(Disease.name == name).one_or_none()

    def get_or_create_mirna(self, name: str) -> MiRNA:
        """Gets an miRNA from the database or creates it if it does not exist

        :param name: A mirBase name
        """
        mirna = self.name_mirna.get(name)
        if mirna is not None:
            return mirna

        mirna = self.get_mirna_by_name(name)
        if mirna is not None:
            self.name_mirna[name] = mirna
            return mirna

        mirna = self.name_mirna[name] = MiRNA(name=name)
        self.session.add(mirna)

        return mirna

    def get_or_create_disease(self, name: str) -> Disease:
        """Get a Disease from the database or creates it if it does not exist

        :param name: A MeSH disease name
        """
        name = name.strip().lower()

        disease = self.name_disease.get(name)
        if disease is not None:
            return disease

        disease = self.get_disease_by_name(name)
        if disease is not None:
            self.name_disease[name] = disease
            return disease

        disease = self.name_disease[name] = Disease(name=name)
        self.session.add(disease)

        return disease

    def count_mirnas(self) -> int:
        """Count the number of miRNAs in the database."""
        return self._count_model(MiRNA)

    def count_diseases(self) -> int:
        """Count the number of diseases in the database."""
        return self._count_model(Disease)

    def count_associations(self) -> int:
        """Count the number of miRNA-disease associations in the database."""
        return self._count_model(Association)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database."""
        return dict(
            mirnas=self.count_mirnas(),
            diseases=self.count_diseases(),
            mirna_disease_associations=self.count_associations(),
        )

    def populate(self, url: Optional[str] = None):
        """Populate the database."""
        df = get_hmdd_df(url=url)

        log.info('building models')
        for _, idx, mirna_name, disease_name, pubmed, description in tqdm(df.itertuples(), total=len(df.index)):
            mirna = self.get_or_create_mirna(mirna_name)
            disease = self.get_or_create_disease(disease_name)

            association = Association(
                pubmed=pubmed,
                description=description,
                mirna=mirna,
                disease=disease,
            )

            self.session.add(association)

        log.info('inserting models')
        self.session.commit()

    def list_associations(self) -> List[Association]:
        """List all associations."""
        return self._list_model(Association)

    def to_bel(self) -> BELGraph:
        """Build a BEL graph containing all of the miRNA-disease associations in the database."""
        graph = BELGraph()

        for association in self.list_associations():
            association.add_to_bel_graph(graph)

        return graph
