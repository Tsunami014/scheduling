import csv

class Item:
    __slots__ = ['nam', 'ppl', 'props']
    def __init__(self, nam):
        self.nam = nam
        self.ppl = 0
        self.props = []

    def add_person(self):
        self.ppl += 1

    def add_prop(self, prop):
        prop.it = self
        self.props.append(prop)

class Scheduler:
    __slots__ = ['ppl', 'items']
    def __init__(self):
        self.ppl = []
        self.items = {}

    def __getitem__(self, k) -> Item:
        return self.items[k]

    def add_person(self, *items, name=None):
        its2 = [i for i in items if i]
        for i in its2:
            if i not in self.items:
                self.items[i] = Item(i)
            self.items[i].add_person()
        self.ppl.append((name, its2))

    def Run(self):
        its = list(self.items.keys())
        return its

    def all_props(self):
        seen = set()
        for it in self.items.values():
            for prop in it.props:
                if prop.nam not in seen:
                    seen.add(prop.nam)
                    yield prop

    def Stats(self, its):
        return [
            prop.nam+': '+prop.score(its) for prop in self.all_props()
        ]

    def __repr__(self): return str(self)
    def __str__(self):
        items = '\n'.join(f"- {i.nam} ({i.ppl} ppl, {len(i.props)} props)" for i in self.items.values())
        return f'<Scheduler with items:\n{items}\n>'

def ReadCSV(fname):
    with open(fname, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        yield from reader
