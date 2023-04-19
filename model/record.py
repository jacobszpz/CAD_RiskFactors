from datetime import datetime
import xml.etree.ElementTree as ET

class Condition:
    def __init__(self, tag):
        attrib = tag.attrib
        self.name = tag.tag
        self.id = attrib['id']
        self.time = attrib['time']
        self.indicator = attrib['indicator']

    def __repr__(self) -> str:
        return f'{self.name}: {self.indicator} @ {self.time}'

class Medication:
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

