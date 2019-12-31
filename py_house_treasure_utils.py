#!/usr/local/bin/python3
# coding: utf-8

#--------------------------------------------- Import Necessary Libraries --------------------------------------------#

import copy
import sys

#-------------------------------------------------- Global Variables -------------------------------------------------#



#---------------------------------------------- Utilities Implementation ---------------------------------------------#

def build_house(file):
	housefp = open("maps/" + file, "r")
	myhouse = []
	line = housefp.readline()
	while line:
		myhouse.append(list(line))
		line = housefp.readline()
	return myhouse


def print_house(h, sr, sc): # house, row, col
	th = copy.deepcopy(h)
	th[sr][sc] = "@"
	print("\n")
	for i in th:
		print(''.join(str(x) for x in i), end='')
	print("\n")


def print_keys(keys):
	at_least_one_k = False
	print("Keys:", end=' ')
	for k in range(0, len(keys)):
		if(keys[k] == True):
			print(str(k) + ", ", end='')
			at_least_one_k = True
	if(not at_least_one_k):
		print("No keys collected...", end='')


def room(h, sr, sc):
	if(h[sr][sc] == '*'): return False
	else: return True


def get_treasure(h, sr, sc):
	if(h[sr][sc] == 't'): return True
	else: return False


def stop():
	print("Sorry, you cant go that way.")


def is_door(h, sr, sc):
	if(h[sr][sc] in ['5','6','7','8','9']): return True
	else: return False


def is_key(h, sr, sc):
	if(h[sr][sc] in ['0','1','2','3','4']): return True
	else: return False


def get_key(h, keys, sr, sc):
	loc = h[sr][sc]
	if(is_key(h, sr, sc)):
		keys[int(loc)] = True
		h[sr][sc] = ' '
	else: return False


def can_unlock(h, keys, sr, sc):
	loc = h[sr][sc]
	if(is_door(h, sr, sc) and keys[int(loc)-5]):
		h[sr][sc] = ' '
		return True
	else:
		return False


def open_door():
	print("You unlocked the door!")

#---------------------------------------------------------------------------------------------------------------------#
