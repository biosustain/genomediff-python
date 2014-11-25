class Metadata(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Metadata({}, {})".format(repr(self.name), repr(self.value))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Record(object):
    def __init__(self, type, id, document=None, parent_ids=None, **extra):
        self.document = document
        self.type = type
        self.id = id
        self.parent_ids = parent_ids
        self._extra = extra

    @property
    def parents(self):
        if not self.parents_ids is None:
            return [self.document[pid] for pid in self.parent_ids]
        else:
            return []

    def __getattr__(self, item):
        return self._extra[item]

    def __repr__(self):
        return "Record('{}', {}, {}, {})".format(self.type,
                                                self.id,
                                                self.parent_ids,
                                                ', '.join('{}={}'.format(k, repr(v)) for k, v in self._extra.items()))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
