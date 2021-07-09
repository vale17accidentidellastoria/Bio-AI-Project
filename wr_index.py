import statistics as st

def age_penalty(val):
    penalty = 0
    if val < 14:
        penalty = 80
    elif 14 <= val < 16:
        penalty = 75
    elif 16 <= val < 18:
        penalty = 55
    elif 0.001 <= val < 0.01:
        penalty = 35
    return penalty

def work_hours_multiplier(val):multi
    multi = 2
    i = 14
    if val > 14:
        multi = 1
    while i >= 0 && i < 15:
        if i==val:
            break   
        i = i -1
        multi = multi + 1 
    return multi


def compute_workers_sustainability_index(country):
    
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
    for c in countries:
        if c == country:
            temp = i
        else:
            i = i + 1

    multiplier = work_hours_multiplier(work_hours[temp])
    begin_age_penalty =age_penalty(begin_age[temp])

    money_ratio = float(salary[temp] / life_cost[temp])

    moltiplication = float(money_ratio * multiplier)

    penalty_percentage = float(( begin_age_penalty * moltiplication ) / 100)

    workers_index = moltiplication - penalty_percentage

    #print("workers_index: ", workers_index)

    return workers_index
