import csv
import pandas as pd

from CONSTANTS import (
    fire_severity_price, available_units, fire_severity_data
)


file_name = 'historical_wildfiredata.csv'

fires = []
with open(file_name, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    fire_records = sorted(csv_reader, key=lambda row: pd.to_datetime(row['timestamp']) - pd.to_datetime(row['fire_start_time']))

    for row in fire_records:
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
        check = True
        for unit in fire_severity_data['high']:
            if available_units[unit]['units_available'] == 0:
                check = False
                break

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
    global total_operational_costs

    severity = fire['severity']

    # checking medium fires
    if severity != 'high':
        if severity == 'medium':
            fire_severity['medium'] += 1
            check = True
            for unit in fire_severity_data['medium']:
                if available_units[unit]['units_available'] == 0:
                    check = False
                    break

            if check:
                cost = 0
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

        # checking low fires
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

# fixing high priority fires first
for fire in fires:
    if fire['severity'] == 'high':
        high_severity(fire)

# shortest time
for fire in fires:
    time_severity(fire)

print(f"Number of fires addressed: {sum(num_fires_addressed.values())}")
print(f"Number of fires delayed: {sum(num_fires_delayed.values())}") 
print(f"Total operational costs: ${total_operational_costs}") 
print(f"Estimated damage costs from delayed responses: ${sum(damage_costs.values())}") 
print(f"Fire severity report: {fire_severity}")