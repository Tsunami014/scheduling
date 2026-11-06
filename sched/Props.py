from abc import ABC, abstractmethod

class Property(ABC):
    __slots__ = ['nam', 'it']
    def __init__(self, nam):
        self.nam = nam

    @property
    def importance(self) -> int:
        return len(self.nam) - len(self.nam.rstrip('!'))

    @abstractmethod
    def score(self, order): ...


class Position(Property):
    __slots__ = ['pos']
    def __init__(self, nam, pos):
        super().__init__(nam)
        self.pos = pos # Pos is 0-1 normalised in the list

    def score(self, order):
        ln = len(order)-1
        return f'{round(abs(self.pos - (order.index(self.it.nam)/ln))*ln)} positions off'


class Group(Property):
    __slots__ = ['oths']
    def __init__(self, nam, oths):
        super().__init__(nam)
        self.oths = oths

    @classmethod
    def group_items(cls, schd, grpnam, names):
        for nam in names:
            schd.items[nam].add_prop(cls(grpnam, [n for n in names if n != nam]))


class SeparateGroup(Group):
    __slots__ = []

    def score(self, order):
        return ''
