map ?= house0.txt
rand ?= houseR.txt
data ?= maps_info.csv

run:
	python3 py_house_treasure.py $(rand) maps/$(data)

runH:
	python3 py_house_treasure.py $(map) maps/$(data)