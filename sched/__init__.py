from collections import defaultdict
import csv

class Item:
    __slots__ = ['ppl', 'props']
    def __init__(self):
        self.ppl = 0
        self.props = []

    def add_person(self):
        self.ppl += 1

    def add_prop(self, prop):
        self.props.append(prop)

class Scheduler:
    __slots__ = ['ppl', 'items']
    def __init__(self):
        self.ppl = []
        self.items = defaultdict(Item)

    def add_person(self, *items, name=None):
        its2 = [i for i in items if i]
        for i in its2:
            self.items[i].add_person()
        self.ppl.append((name, its2))

    def freeze(self):
        self.items = dict(self.items)

    def Run(self):
        its = list(self.items.keys())
        return its

    def __repr__(self): return str(self)
    def __str__(self):
        items = '\n'.join(f"- {nam} ({i.ppl} ppl, {len(i.props)} props)" for nam, i in self.items.items())
        return f'<Scheduler with items:\n{items}\n>'

def ReadCSV(fname):
    with open(fname, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        yield from reader
