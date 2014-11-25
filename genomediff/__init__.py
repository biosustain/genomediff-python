import itertools
from genomediff.parser import GenomeDiffParser
from genomediff.records import Metadata


class GenomeDiff(object):

    def __init__(self):
        self.metadata = {}
        self.mutations = []
        self.evidence = []
        self.validation = []
        self._index = {}

    @classmethod
    def read(cls, fsock):
        gd = GenomeDiff()

        for record in GenomeDiffParser(document=gd, fsock=fsock):
            if isinstance(record, Metadata):
                gd.metadata[record.name] = record.value
            else:
                if len(record.type) == 3:
                    gd.mutations.append(record)
                if len(record.type) == 2:
                    gd.evidence.append(record)
                if len(record.type) == 4:
                    gd.validation.append(record)
                gd._index[record.id] = record
        return gd

    def __getitem__(self, item):
        return self._index[item]

    def write(self, fsock):
        raise NotImplementedError()

    def __len__(self):
        return len(self.mutations) + len(self.evidence) + len(self.validation)

    def __iter__(self):
        return itertools.chain(self.mutations, self.evidence, self.validation)