"""
Module that parses the n2c2 2014 dataset
"""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


class Condition:
    """Represents a tag belonging to a condition."""
    def __init__(self, tag):
        attrib = tag.attrib
        self.name = tag.tag
        self.id = attrib['id']
        self.time = attrib['time']
        self.indicator = attrib['indicator']

    def __repr__(self) -> str:
        return f'{self.name}: {self.indicator} @ {self.time}'


class Medication:
    """Represents a tag corresponding to a medication."""
    def __init__(self, tag):
        attrib = tag.attrib
        self.id = attrib['id']
        self.time = attrib['time']
        self.types = [t for t in [attrib[i] for i in ['type1', 'type2']] if t]

    def __repr__(self) -> str:
        return f'{self.types} @ {self.time}'


class Record:
    """Parse and represent a medical record."""

    c = ('HYPERLIPIDEMIA', 'OBESE', 'HYPERTENSION', 'DIABETES', 'CAD')

    def __init__(self, filename: str):
        """Read from XML file"""
        self._tree = ET.parse(filename)
        self._root = self._tree.getroot()

        try:
            date_text = self._root[0].text.strip()[13:23]
            self.date = datetime.fromisoformat(date_text).date()
        except ValueError as e:
            self.date = None

        self.factors = []
        self.medicines = []
        self.fam_hist = False
        self.smoker = "unknown"

        # Iterate over tags
        for annot in self._root[1]:
            if annot.tag in self.c:
                self.factors.append(Condition(annot))
            elif annot.tag == 'MEDICATION':
                self.medicines.append(Medication(annot))
            elif annot.tag == 'SMOKER':
                self.smoker = annot.attrib['status']
            elif annot.tag == 'FAMILY_HIST':
                self.fam_hist = annot.attrib['indicator'] == 'present'

    @property
    def text(self) -> str:
        return self._root[0].text

    def __repr__(self) -> str:
        return f'RF: {len(self.factors)}, M: {len(self.medicines)}'

    def __str__(self) -> str:
        return (
            f'Record @ {self.date}\n'
            f'Risk factors: {[x.name for x in self.factors]}\n'
            f'Medications: {self.medicines}\n'
            f'Smoker: {self.smoker}\n'
            f'Family history: {self.fam_hist}'
        )


class Patient:
    """Represents a patient with a collection of records."""

    def __init__(self, pt_id: str):
        self.pt_id = pt_id
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def factor_indicator(self, disease: str, indicator: str) -> bool:
        """
        Check patient records and return True if the disease is
        annotated under the specified indicator.
        """
        for r in self.records:
            for rf in r.factors:
                if rf.name == disease and rf.indicator == indicator:
                    return True
        return False

    @property
    def text(self) -> str:
        """Collection of free text from all records"""
        return ''.join([x.text for x in self.records])


class Dataset:
    """
    Represents a directory with medical records from the n2c2 2014 challenge.
    """

    def __init__(self, directory: str | Path):
        self.patients = {}

        for file_path in Path(directory).iterdir():
            if file_path.is_file():
                pt_id = file_path.name.split('-')[0]

                if pt_id not in self.patients:
                    self.patients[pt_id] = Patient(pt_id)

                self.patients[pt_id].add_record(Record(file_path))
        print(f'Read {len(self.patients)} patients')

    def __getitem__(self, index):
        return list(self.patients.values())[index]
    
    def labels(self, condition: str, indicator: str) -> list[int]:
        """Extract condition labels for each patient (1 if condition is present, else 0)"""
        return [int(pt.factor_indicator(condition, indicator)) for pt in self.patients.values()]

    @property
    def texts(self) -> list[str]:
        """The list of combined free texts of each patient."""
        return [patient.text for patient in self.patients.values()]

    def print_data(self) -> None:
        for patient in self.patients:
            print(f'Records for patient {patient}')

            for record in self.patients[patient].records:
                print(record)
            print()

