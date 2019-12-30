#!/usr/local/bin/python3
# coding: utf-8

"""
Title: py_house_treasure.py
Author(s): Jonathan A. Gibson
Description:

Goals:
  1. Be able to play multiple different house maps. Store all in "maps" directory with set CSV info to import.
  2. Let user choose the house map at the command line, or choose to play a random map.
  3. Display the key array to the user based on the total number of keys, not all 5 if there are not 5 keys on the map.
  4. Display the key inventory in a more friendly way rather than just a 0-based array.
  5. 
  6. 
Notes:
  > 
"""

#--------------------------------------------- Import Necessary Libraries --------------------------------------------#

import sys
import math
import random
import os.path
import pandas as pd
import py_house_treasure_utils as phtu

#---------------------------------------------- Define Main Functionality --------------------------------------------#

def main():

	# Load the CSV data for the maps
	metadata = sys.argv[2]
	if(os.path.exists(metadata)):
		print("\nLoading map data...")
		maps_df = pd.read_csv(metadata)
		print("Done.")
	else:
		print("ERROR::002::FILE_NOT_FOUND")
		print("Map metadata not found. Please provide valid CSV data for each house map.\n")
		print("For guidance on building a CSV data file, see \'maps/maps_info.csv\'.\n")
		print("Program run command should follow the following format: \"python3 py_house_treasure.py <house_file_name>.txt maps/<map_data>.csv\" or use one of the default \"Makefile\" commands.\n")
		sys.exit()

	# Print the program command line arguments
	print("\nProgram Name:", sys.argv[0])
	print("Number of command line arguments:", len(sys.argv))
	print("The command line argument(s) are:", str(sys.argv), '\n')

	# Determine if we need to pull random house data or just the data about the file from the command line argument
	if(sys.argv[1] == "houseR.txt"):
		hfs = "house"
		valid_rows = len(maps_df.index) - 1 # exclude the "houseR.txt" row
		r_int = random.randint(0, valid_rows - 1) # remove the inclusivity of the "randint()" function on the upper bound
		hfs += str(r_int)
		hfs += ".txt"
		chosen_map = hfs
	else:
		chosen_map = sys.argv[1]

	# Get the correct house (map) data
	for idx, row in maps_df.iterrows():
		if(row["HOUSE_FILE"] == chosen_map):
			map_data = maps_df.iloc[idx,:]
			print(map_data)

	# Initialize variables
	keys = [False] * int(map_data["NUM_KEYS"])
	num_treasures = int(map_data["NUM_TREASURES"]) # total number of treasures in the house
	t_count = 0 # number of treasures found
	t_loc = False # if location is a treasure ; if there is a 't' in our way or not
	k_loc = False # if location is a key
	passage = False # if can go through door
	valid_move = False # a '*' in our way
	quit = False

	# Read the house file into a matrix (list of lists)
	house = phtu.build_house(map_data["HOUSE_FILE"]) 

	# Set the spawn location
	spawn_r = int(map_data["SPAWN_ROW"])
	spawn_c = int(map_data["SPAWN_COL"])

	# Print instructions
	print("\nMove around the house by entering \'W\' for North, \'S\' for South, \'A\' for East, or \'D\' for West.")
	print("You cannot move through walls (marked by the \'*\' characters).")
	print("Find the keys and collect all the treaure!")
	phtu.print_house(house, spawn_r, spawn_c)

	# Set the current and travel locations
	trav_r = cur_r = spawn_r
	trav_c = cur_c = spawn_c

	while(t_count < num_treasures):
		command = input("Move: ").upper()
		print("Keys:", keys)

		# Reset the travel indices
		trav_r = cur_r
		trav_c = cur_c

		if(command == 'W'):
			trav_r = cur_r - 1
		elif(command == 'S'):
			trav_r = cur_r + 1
		elif(command == 'A'):
			trav_c = cur_c - 1
		elif(command == 'D'):
			trav_c = cur_c + 1
		elif(command == "QUIT"):
			quit = True
			break
		else:
			print("Not a valid direction, try again.")
			continue

		loc = house[trav_r][trav_c]
		valid_move = phtu.room(house, trav_r, trav_c)
		t_loc = phtu.get_treasure(house, trav_r, trav_c)
		k_loc = phtu.get_key(house, keys, trav_r, trav_c)
		passage = phtu.can_unlock(house, keys, trav_r, trav_c)

		# If we are picking up treasure
		if(t_loc):
			house[trav_r][trav_c] = ' '
			t_count += 1

		# If we are accessing a door
		if(passage): phtu.open_door()

		# Cant go through door if dont have proper key
		if(phtu.is_door(house, trav_r, trav_c) and not keys[int(loc)-5]):
			valid_move = False

		if(not valid_move): phtu.stop()
		else:
			cur_r = trav_r
			cur_c = trav_c

		phtu.print_house(house, cur_r, cur_c)

	if(not quit and t_count >= num_treasures):
		print("Congrats, you found all the treasure!")
	else:
		print("You quit the game.")


main() # call the main function