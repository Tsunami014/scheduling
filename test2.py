from sched import Scheduler, ReadCSV, Props
from random import random, randint
FILE = 'test2.csv'

# Generate
nams = ["Programming", "Woodworking", "Hardware"]
mxlvl = 3
maxcols = 3
with open(FILE, 'w+') as f:
    for i in range(80):
        row = [f"Person{i}"]
        lvl = randint(1, mxlvl)
        avail = nams.copy()
        for _ in range(randint(1, maxcols-1)):
            nam = avail.pop(randint(0, len(avail)-1))
            if random() < 0.1:
                if lvl > 1 and (lvl >= mxlvl or random() > 0.5):
                    row.append(f"lvl {lvl-1} {nam}")
                else:
                    row.append(f"lvl {lvl+1} {nam}")
            else:
                row.append(f"lvl {lvl} {nam}")
        row += ['' for _ in range(maxcols-len(row))]
        f.write(','.join(row)+'\n')

# Test generated
schd = Scheduler()
for nam, *subjs in ReadCSV(FILE):
    schd.add_person(*subjs)
# print(schd)

for nam in nams:
    schd[(f"lvl {lvl} {nam}" for lvl in range(1, mxlvl+1))].aka(nam)
    schd.allknownas(nam).add_prop(Props.SeparateGroup("Separate "+nam, [nam]))
for lvl in range(1, mxlvl+1):
    aka = f"lvl {lvl}"
    schd[(f"lvl {lvl} {nam}" for nam in nams)].aka(aka)
    schd.allknownas(aka).add_prop(Props.SeparateGroup(f"Separate lvl {lvl}", [aka]))
print(schd)
print()

schd.JustWork()
