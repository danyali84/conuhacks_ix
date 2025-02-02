import csv
import pandas as pd

from CONSTANTS import (
    fire_severity_price, available_units, fire_severity_data
)

file_name = 'current_wildfiredata.csv'

fires = []
with open(file_name, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        fires.append({
            'timestamp': row['timestamp'],
            'fire_start_time': row['fire_start_time'],
            'location': row['location'],
            'severity': row['severity']
        })


num_fires_addressed = {'low': 0, 'medium': 0, 'high': 0}
num_fires_delayed = {'low': 0, 'medium': 0, 'high': 0}
total_operational_costs = 0
damage_costs = {'low': 0, 'medium': 0, 'high': 0}
fire_severity = {'low': 0, 'medium': 0, 'high': 0}

g_timestamp = pd.to_datetime('2020-01-10')
g_start_time = pd.to_datetime('2020-01-10')
low_deployed = ''


def deploy(timestamp, start_time, fire):
    global total_operational_costs
    global g_timestamp
    global same_date_count

    severity = fire['severity']

    update(severity, start_time)

    if severity == 'high':
        fire_severity['high'] += 1
        check = True
        for unit in fire_severity_data['high']:
            if available_units[unit]['units_available'] == 0:
                check = False
                break

        if check:
            cost = 0
            g_timestamp = pd.to_datetime(timestamp)
            
            num_fires_addressed['high'] += 1
            for unit in fire_severity_data['high']:
                available_units[unit]['units_available'] -= 1
                cost += available_units[unit]['operation_cost']
            total_operational_costs += cost
        
        else:
            num_fires_delayed['high'] += 1
            damage_costs['high'] += fire_severity_price['high']

    elif severity == 'medium':
        fire_severity['medium'] += 1
        check = True
        for unit in fire_severity_data['medium']:
            if available_units[unit]['units_available'] == 0:
                check = False
                break

        if check:
            g_timestamp = pd.to_datetime(timestamp)
            cost = 0

            num_fires_addressed['medium'] += 1
            for unit in fire_severity_data['medium']:
                available_units[unit]['units_available'] -= 1
                cost += available_units[unit]['operation_cost']
            total_operational_costs += cost
        else:
            if available_units['helicopters']['units_available'] >0:
                g_timestamp = pd.to_datetime(timestamp)
                num_fires_addressed['medium'] += 1
                available_units['helicopters']['units_available'] -= 1
                total_operational_costs += available_units['helicopters']['operation_cost']
            else:
                num_fires_delayed['medium'] += 1
                damage_costs['medium'] += fire_severity_price['medium']

    elif severity == 'low':
        deployed = ''
        check = False
        fire_severity['low'] += 1
        for deployments in fire_severity_data['low']:
            if available_units[deployments]['units_available'] > 0:
                check = True
                deployed = deployments
                available_units[deployed]['units_available'] -= 1
                break

        if check:
            g_timestamp = pd.to_datetime(timestamp)
            num_fires_addressed['low'] += 1
            total_operational_costs += available_units[deployed]['operation_cost']
        else:
            num_fires_delayed['low'] +=1
            damage_costs['low'] += fire_severity_price['low']


def update(severity, time):
    if g_timestamp < pd.to_datetime(time):
        if severity == 'low' and low_deployed != '':
            available_units[low_deployed]['units_available'] += 1
        elif (severity == 'medium') or (severity == 'high') :
            for deployments in fire_severity_data[severity]:
                available_units[deployments]["units_available"] += 1

for fire in fires:
    deploy(fire['timestamp'], fire['fire_start_time'], fire)


print(f"Number of fires addressed: {sum(num_fires_addressed.values())}")
print(f"Number of fires delayed: {sum(num_fires_delayed.values())}") 
print(f"Total operational costs: ${total_operational_costs}") 
print(f"Estimated damage costs from delayed responses: ${sum(damage_costs.values())}") 
print(f"Fire severity report: {fire_severity}")