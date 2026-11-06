from random import shuffle, randint, random
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

    def score(self, order):
        if len(self.props) == 0:
            return 0
        return sum(max(min(p.score(order), 1), 0) for p in self.props)/len(self.props) * self.ppl

    def desc(self):
        return f'{self.nam} [{self.ppl} ppl]'

    def __str__(self): return self.nam
    def __repr__(self):
        xtra = f" (aka {','.join(self.tags)})" if self.tags else ''
        return f'{self.nam}{xtra} [{self.ppl} ppl, {len(self.props)} props]'

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

    def score(self, order):
        return sum(it.score(order) for it in self.items)/sum(it.ppl for it in self.items) * 100

    def Run(self):
        print("Running...\nCtrl+C to print best/quit")
        best = None
        bestsco = None
        run = True
        while run:
            try:
                if best is not None and random() < 0.15: # Every now and then retry the best one
                    its = best.copy()
                else:
                    its = self.items.copy()
                    shuffle(its)
                thisbestsco = None
                thisbest = None
                lastimprov = 0
                trials = 0
                while trials < 10:
                    while lastimprov < 50:
                        sco = self.score(its)
                        if bestsco is None or sco > bestsco:
                            bestsco = sco
                            best = its.copy()
                            print(f"New best: {bestsco}")
                        if thisbestsco is None or sco > thisbestsco:
                            thisbestsco = sco
                            lastimprov = 0
                            thisbest = its.copy()
                            trials = 0
                        else:
                            lastimprov += 1
                        # Slightly modify the order by moving an item
                        it = its.pop(randint(0, len(its)-1))
                        its.insert(randint(0, len(its)-1), it)
                    its = thisbest
                    trials += 1
            except KeyboardInterrupt:
                print('\nScheduled order:\n'+'\n'.join(f'- {i}' for i in best)+'\n')
                self.PrintStats(best)
                run = input("Continue? [y/n] > ").lower() != 'n'
        return best

    def all_props(self):
        seen = set()
        for it in self.items:
            for prop in it.props:
                if prop.nam not in seen:
                    seen.add(prop.nam)
                    yield prop

    def Stats(self, its, full=False):
        return [
            prop.nam+' - '+prop.scorestr(its, full) for prop in self.all_props()
        ]
    def PrintStats(self, its, full=False):
        print('Stats:\n'+'\n'.join('* '+i for i in sorted(self.Stats(its, full))))

    def __repr__(self): return str(self)
    def __str__(self):
        items = '\n'.join("- "+repr(i) for i in sorted(self.items, key=lambda x: x.nam))
        return f'<Scheduler with items:\n{items}\n>'

def ReadCSV(fname):
    with open(fname, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        yield from reader
