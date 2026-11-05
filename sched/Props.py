from abc import ABC, abstractmethod

class Property(ABC):
    __slots__ = []

class Group(Property):
    __slots__ = ['nam', 'oths']
    def __init__(self, nam, oths):
        self.nam = nam
        self.oths = oths

    @classmethod
    def group_items(cls, schd, grpnam, names):
        for nam in names:
            schd.items[nam].add_prop(cls(grpnam, [n for n in names if n != nam]))

class SeparateGroup(Group):
    __slots__ = []
