c = 'india'

workers_info = open("workersfile.txt")
info = workers_info.readlines()

countries = []
salary = []
life_cost = []
work_hours = []
begin_age = []

for element in info:
    countries.append(element.split('\t')[0])
    salary.append(element.split('\t')[1])
    life_cost.append(element.split('\t')[2])
    work_hours.append(element.split('\t')[3])
    begin_age.append(element.split('\t')[4])

i = 0
temp = 0    
for country in countries:
    if country == c:
        temp = i
    else:
        i = i + 1

print(countries[temp])
print(work_hours[temp])
print(begin_age[temp])
print(salary[temp])
print(life_cost[temp])
