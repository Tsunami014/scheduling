import csv

class Item:
    __slots__ = ['nam', 'ppl', 'props', 'tags']
    def __init__(self, nam):
        self.nam = nam
        self.ppl = 0
        self.props = []
        self.tags = []

    def add_person(self):
        self.ppl += 1

    def add_prop(self, prop):
        prop.it = self
        self.props.append(prop)
        return self

    def aka(self, *nams):
        self.tags.extend(nams)
        return self

    def isknownas(self, nam):
        return self.nam == nam or nam in self.tags

    def __str__(self): return self.nam
    def __repr__(self):
        xtra = f" (aka {','.join(self.tags)})" if self.tags else ''
        return f'{self.nam}{xtra} <{self.ppl} ppl, {len(self.props)} props>'

class ItemGroup:
    __slots__ = ['its']
    def __init__(self, *its):
        self.its = [i for i in its if i is not None]

    def __getattr__(self, nam):
        if nam in (
            'aka', 'add_prop'
        ):
            def fn(*args):
                for it in self.its:
                    getattr(it, nam)(*args)
                return self
            return fn
        super().__getattr__(nam)

class Scheduler:
    __slots__ = ['ppl', 'items']
    def __init__(self):
        self.ppl = []
        self.items = []

    def __getitem__(self, k) -> Item:
        if isinstance(k, str):
            for it in self.items:
                if it.nam == k:
                    return it
            return None
        grp = ItemGroup()
        for it in k:
            nit = self[it]
            if nit is not None:
                grp.its.append(nit)
        return grp

    def allknownas(self, nam):
        out = None
        for it in self.items:
            if it.isknownas(nam):
                if out is None:
                    out = it
                elif isinstance(out, Item):
                    out = ItemGroup(out, it)
                else:
                    out.its.append(it)
        return out

    def add_person(self, *items, name=None):
        its2 = [i for i in items if i]
        for i in its2:
            it = self[i]
            if it is None:
                it = Item(i)
                self.items.append(it)
            it.add_person()
        self.ppl.append((name, its2))

    def Run(self):
        return self.items

    def all_props(self):
        seen = set()
        for it in self.items:
            for prop in it.props:
                if prop.nam not in seen:
                    seen.add(prop.nam)
                    yield prop

    def Stats(self, its):
        return [
            prop.nam+' - '+prop.score(its) for prop in self.all_props()
        ]

    def JustWork(self):
        print("Running scheduler...")
        result = self.Run()
        print('\nScheduled order:\n'+'\n'.join(f'- {i}' for i in result))
        print('\nStats:\n'+'\n'.join('* '+i for i in self.Stats(result)))
        return result

    def __repr__(self): return str(self)
    def __str__(self):
        items = '\n'.join("- "+repr(i) for i in sorted(self.items, key=lambda x: x.nam))
        return f'<Scheduler with items:\n{items}\n>'

def ReadCSV(fname):
    with open(fname, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        yield from reader
