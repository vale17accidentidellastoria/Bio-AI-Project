import statistics as st

def age_penalty(val):
    penalty = 0
    if int(val) < 14:
        penalty = 80    
    elif 14 <= int(val) < 16:
        penalty = 75
    elif 16 <= int(val) < 18:
        penalty = 55
    elif int(val) >= 18:
        penalty = 35
    return penalty

def work_hours_multiplier(val):
    multiplier = 2
    hours= 14
    if int(val) > 14:
        multiplier = 1

    while hours >= 0 and hours < 15 and hours != int(val):   
        hours = hours - 1
        multiplier = multiplier + 1 
    return multiplier

def compute_workers_sustainability_index(country):
    
    workers_info = open("workersfile.txt")
    info = workers_info.readlines()

    countries = []
    salary = []
    life_cost = []
    work_hours = []
    begin_age = []

    for element in info:
        value = element.split('\t')
        countries.append(value[0])
        salary.append(value[1])
        life_cost.append(value[2])
        work_hours.append(value[3])
        begin_age.append(value[4].replace("\n",""))

    i = 0
    temp = 0  
    for c in countries:
        if c == country:
            temp = i
        else:
            i = i + 1

    multiplier = work_hours_multiplier(int(work_hours[temp]))
    begin_age_penalty =age_penalty(begin_age[temp])

    money_ratio = float(int(salary[temp]) / int(life_cost[temp]))

    moltiplication = float(money_ratio * multiplier)

    penalty_percentage = float(( begin_age_penalty * moltiplication ) / 100)

    workers_index = moltiplication - penalty_percentage

    return round(workers_index, 2)
