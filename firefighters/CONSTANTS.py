# data for each type of deployments
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

fire_severity_price = {
    'low' : 50000,
"medium" : 100000,
"high" : 200000
}

available_units = {
    'smoke_jumpers': {'deployment_time': smoke_jumper_dep, 'operation_cost': smoke_jumper_op, 'units_available': smoke_jumper_unit},
    'fire_engines': {'deployment_time': fire_engine_dep, 'operation_cost': fire_engine_op, 'units_available': fire_engine_unit},
    'helicopters': {'deployment_time': helicopter_dep, 'operation_cost': helicopter_op, 'units_available': helicopter_unit},
    'tanker_planes': {'deployment_time': tanker_dep, 'operation_cost': tanker_op, 'units_available': tanker_unit},
    'ground_crews': {'deployment_time': ground_crew_dep, 'operation_cost': ground_crew_op, 'units_available': ground_crew_unit}
}


fire_severity_data = {
    'low' : ['ground_crews', 'fire_engines', 'helicopters', 'tanker_planes'],
    'medium' : ['fire_engines', 'ground_crews'],
    'high' : ['tanker_planes', 'helicopters', 'ground_crews']
}