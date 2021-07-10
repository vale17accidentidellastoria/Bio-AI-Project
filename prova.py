workers_info = open("workersfile.txt")
info = workers_info.readlines()

countries = []
salary = []
life_cost = []
age = []
work = []

for line in info:
	countries.append(line.split('\t')[0])
	salary.append(line.split('\t')[1])
	life_cost.append(line.split('\t')[2])
	age.append(line.split('\t')[3])
	work.append(line.split('\t')[4])

print("countries: ", countries) 
print("s: ", salary)
print("lc: ", life_cost)
print("age: ", age)
print("work: ", work)

