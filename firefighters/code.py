import csv
from collections import defaultdict
import pandas as pd

from CONSTANTS import (
    fire_severity_price, available_units, fire_severity_data
)


file_name = 'historical_wildfiredata.csv'

fires = []
with open(file_name, 'r') as csv_file:
    df = pd.read_csv(csv_file)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['fire_start_time'] = pd.to_datetime(df['fire_start_time'])

    # difference
    df['received'] = df['timestamp'] - df['fire_start_time']

    df_sorted = df.sort_values(by='received')

#IDFK il est 3am i just copy pasted from AI kms
    for _, row in df_sorted.iterrows():
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


def high_severity(fire):
    global total_operational_costs

    severity = fire['severity']
    cost = 0

    if severity == 'high':
        fire_severity['high'] += 1
        check = all(available_units[unit]['units_available'] > 0 for unit in fire_severity_data['high'])

        if check:
            num_fires_addressed['high'] += 1
            for unit in fire_severity_data['high']:
                available_units[unit]['units_available'] -= 1
                cost += available_units[unit]['operation_cost']
            total_operational_costs += cost
            return True
        else:
            num_fires_delayed['high'] += 1
            damage_costs['high'] += fire_severity_price['high']
            return False

def time_severity(fire):
    cost = 0
    severity = fire['severity']

    if severity == 'medium':
        fire_severity['medium'] += 1
        check = all(available_units[unit]['units_available'] > 0 for unit in fire_severity_data['medium'])

        if check:
            num_fires_addressed['medium'] += 1
            for unit in fire_severity_data['medium']:
                available_units[unit]['units_available'] -= 1
                cost += available_units[unit]['operation_cost']
            total_operational_costs += cost
        else:
            if available_units['helicopters']['units_available'] >0:
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
            num_fires_addressed['low'] += 1
            total_operational_costs += available_units[deployed]['operation_cost']
        else:
            num_fires_delayed['low'] +=1
            damage_costs['low'] += fire_severity_price['low']
           

#high severity
    for fire in fires:
        if fire['severity'] == 'high':
            if high_severity(fire):
                fires.remove(fire)
    
#shortest time
    for fire in fires:
        # TODO: implement function that just reads the variables
        # table should already have been ordered

        time_severity(fire)

    # for resource_name, resource_data in available_units.items():

    #     if resource_data['units_available'] > 0:
    #         cost = resource_data['operation_cost']
    #         if cost < min_cost:
    #             optimal_resource = resource_name
    #             min_cost = cost

    # if optimal_resource:
    #     available_units[optimal_resource]['units_available'] -= 1
    #     total_operational_costs += available_units[optimal_resource]['operation_cost']
    #     num_fires_addressed[severity] += 1
    #     fire_severity[severity] += 1

    # else:
    #     num_fires_delayed[severity] += 1
    #     damage_cost = fire_severity_data[severity]
    #     total_operational_costs += damage_cost
    #     damage_costs[severity] = damage_cost

print(f"Number of fires addressed: {sum(num_fires_addressed.values())}")
print(f"Number of fires delayed: {sum(num_fires_delayed.values())}") 
print(f"Total operational costs: ${total_operational_costs}") 
print(f"Estimated damage costs from delayed responses: ${sum(damage_costs.values())}") 
print(f"Fire severity report: {fire_severity}")