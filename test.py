from sched import Scheduler, ReadCSV, Props

schd = Scheduler()
for nam, *subjs in ReadCSV('test.csv'):
    schd.add_person(*subjs)
schd.freeze()

Props.SeparateGroup.group_items(schd, "Maths", ["Maths1", "Maths2"])
print(schd)

print("\nRunning scheduler...")
result = schd.Run()
print('\nScheduled:\n'+'\n'.join('- '+i for i in result))
