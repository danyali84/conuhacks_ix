
smoke_jumper_dep=30
smoke_jumper_op=5000
smoke_jumper_unit=5

fire_engine_dep=60
fire_engine_op=2000
fire_engine_unit=10

helicopter_dep=45
helicopter_op=10000
helicopter_unit=3

tanker_dep=120
tanker_op=15000
tanker_unit=2

ground_crew_dep=90
ground_crew_op=3000
ground_crew_unit=8

low=50000
medium=100000
high=200000

with open('historical_wildfiredata.csv','r') as file:
    data = file.read()
    print(data)