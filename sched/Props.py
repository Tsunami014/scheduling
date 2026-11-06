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
        return f'{round(abs(self.pos - (order.index(self.it)/ln))*ln)} positions off'


class Group(Property):
    __slots__ = ['aparts']
    def __init__(self, nam, aparts):
        super().__init__(nam)
        self.aparts = aparts


class SeparateGroup(Group):
    __slots__ = []

    def score(self, order):
        dist = None
        mx = None
        prev = None
        for it in order:
            if any(it.isknownas(i) for i in self.aparts):
                if prev is not None:
                    if mx is None or dist >= mx[0]:
                        if mx is None or dist > mx[0]:
                            mx = (dist, [(prev, it.nam)])
                        else:
                            mx[1].append((prev, it.nam))
                prev = it.nam
                dist = 0
            elif dist is not None:
                dist += 1
        if mx is None:
            return 'None found'
        if len(mx[1]) == 1:
            return f'Closest: {mx[1][0]} ({mx[0]} apart)'
        return f'{len(mx[1])} closests: {mx[1]} (all {mx[0]} apart)'
