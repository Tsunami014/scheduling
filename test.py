from sched import Scheduler, ReadCSV, Props
from random import randint, choice

# Generate
subjs = ['Maths1', 'Maths2', 'English', 'History', 'Software', 'Drama']
maxcols = 5
with open('test.csv', 'w+') as f:
    for i in range(50):
        row = [f"Person{i}"]
        row += [choice(subjs) for _ in range(randint(1, 4))]
        row += ['' for _ in range(maxcols-len(row))]
        f.write(','.join(row)+'\n')

# Test generated
schd = Scheduler()
for nam, *subjs in ReadCSV('test.csv'):
    schd.add_person(*subjs)
schd.freeze()

Props.SeparateGroup.group_items(schd, "Maths", ["Maths1", "Maths2"])
print(schd)

print("\nRunning scheduler...")
result = schd.Run()
print('\nScheduled:\n'+'\n'.join('- '+i for i in result))
