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
    @abstractmethod
    def scorestr(self, order, full): ...


class Position(Property):
    __slots__ = ['pos']
    def __init__(self, nam, pos):
        super().__init__(nam)
        self.pos = pos # Pos is 0-1 normalised in the list

    def score(self, order):
        ln = len(order)-1
        return abs(self.pos - (order.index(self.it)/ln))
    def scorestr(self, order, _):
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
                            mx = [dist, 1]
                        else:
                            mx[1] += 1
                prev = it.desc()
                dist = 0
            elif dist is not None:
                dist += 1
        if mx is None:
            return 0
        return ((mx[0]*mx[1]) /
            (len(order)*sum(int(any(it.isknownas(i) for i in self.aparts)) for it in order))
        )

    def scorestr(self, order, full):
        dist = None
        mx = None
        prev = None
        for it in order:
            if any(it.isknownas(i) for i in self.aparts):
                if prev is not None:
                    if mx is None or dist >= mx[0]:
                        if mx is None or dist > mx[0]:
                            mx = (dist, [(prev, it.desc())])
                        else:
                            mx[1].append((prev, it.desc()))
                prev = it.desc()
                dist = 0
            elif dist is not None:
                dist += 1
        if mx is None:
            return 'None found'
        if not full:
            return f'{len(mx[1])} closests, {mx[0]} apart'
        if len(mx[1]) == 1:
            return f'Closest: {mx[1][0]}\n\t({mx[0]} apart)'
        return f'{len(mx[1])} closests: {mx[1]}\n\t(all {mx[0]} apart)'
