import csv
import os
from collections import defaultdict

smoke_jumper_dep = 30
smoke_jumper_op = 5000
smoke_jumper_unit = 5

fire_engine_dep = 60
fire_engine_op = 2000
fire_engine_unit = 10

helicopter_dep = 45
helicopter_op = 10000
helicopter_unit = 3

tanker_dep = 120
tanker_op = 15000
tanker_unit = 2

ground_crew_dep = 90
ground_crew_op = 3000
ground_crew_unit = 8


fire_severity_data = {
    'low' : 50000,
"medium" : 100000,
"high" : 200000
}

file_name = 'historical_wildfiredata.csv'

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


available_units = {
    'smoke_jumpers': {'deployment_time': smoke_jumper_dep, 'operation_cost': smoke_jumper_op, 'units_available': smoke_jumper_unit},
    'fire_engines': {'deployment_time': fire_engine_dep, 'operation_cost': fire_engine_op, 'units_available': fire_engine_unit},
    'helicopters': {'deployment_time': helicopter_dep, 'operation_cost': helicopter_op, 'units_available': helicopter_unit},
    'tanker_planes': {'deployment_time': tanker_dep, 'operation_cost': tanker_op, 'units_available': tanker_unit},
    'ground_crews': {'deployment_time': ground_crew_dep, 'operation_cost': ground_crew_op, 'units_available': ground_crew_unit}
}

num_fires_addressed = {'low': 0, 'medium': 0, 'high': 0}
num_fires_delayed = {'low': 0, 'medium': 0, 'high': 0}
total_operational_costs = 0
damage_costs = {'low': 0, 'medium': 0, 'high': 0}
fire_severity = {'low': 0, 'medium': 0, 'high': 0}

def high_severity(fire):
    global total_operational_costs