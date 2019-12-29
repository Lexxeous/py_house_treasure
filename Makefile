map ?= house1.txt
rand ?= houseR.txt
data ?= maps_info.csv

run:
	python3 py_house_treasure.py $(map) maps/$(data)

runR:
	python3 py_house_treasure.py $(rand) maps/$(data)