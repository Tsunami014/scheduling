from sched import Scheduler, ReadCSV, Props
from random import random, randint
FILE = 'test.csv'

# Generate
xtras = ['History', 'Software', 'Drama', 'Physics', 'Economics']
maxcols = 6
with open(FILE, 'w+') as f:
    for i in range(80):
        row = [f"Person{i}", 'English']
        if random() >= 0.2:
            row.append('Maths1')
            if random() >= 0.7:
                row.append('Maths2')
        avxtras = xtras.copy()
        while avxtras and len(row) < maxcols and (len(row) <= 2 or random() > 0.4):
            row.append(avxtras.pop(randint(0, len(avxtras)-1)))
        row += ['' for _ in range(maxcols-len(row))]
        f.write(','.join(row)+'\n')

# Test generated
schd = Scheduler()
for nam, *subjs in ReadCSV(FILE):
    schd.add_person(*subjs)
# print(schd)

schd['Maths1', 'Maths2'].aka('Maths')
schd['Physics'].add_prop(Props.Position('Make physics last', 1))
schd.allknownas('Maths').add_prop(Props.SeparateGroup("Separate maths", ["Maths"]))
print(schd)
print()

schd.JustWork()
