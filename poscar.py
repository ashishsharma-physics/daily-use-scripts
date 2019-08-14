#!/usr/bin/env python
# -*- coding: utf-8 -*-

# * POSCAR Output
# * by En Wang, SF10, IOP, CAS (enwang@iphy.ac.cn)

import re
import click
import numpy as np

class POSCAR:

	def __init__(self, POSCAR):
		file = open(POSCAR)
		# First line usally is the 'name' of the system
		self.name = file.readline().strip()
		# Second line provides a universal scaling factor
		self.scaling = eval(file.readline().strip())
		# Three lattice vectors
		self.a = [eval(i) for i in file.readline().split()]
		self.b = [eval(i) for i in file.readline().split()]
		self.c = [eval(i) for i in file.readline().split()]
		self.lat = [self.a, self.b, self.c]
		# The number of atom per atomic species
		tmp = file.readline()
		# if line is atomic species name, read next line to get number
		if re.search('[a-zA-Z]', tmp):
			self.atom_num = [eval(i) for i in file.readline().split()]
			self.atom_species = tmp.split()
		else:
			self.atom_num = [eval(i) for i in tmp]
			self.atom_species = [''] * len(self.atom_num)
		# Selective dynamics tag, optional
		tmp = file.readline()
		if len(tmp.strip()) == 0:
			pass
		elif tmp.strip().upper()[0] == 'S':
			self.is_selective_dynamic = True
			line = file.readline()
			if line.strip().upper()[0] in ['C', 'K']:
				self.is_cartesian = True
			else:
				self.is_cartesian = False
		elif tmp.strip().upper()[0] in ['C', 'K']:
			self.is_selective_dynamic = False
			self.is_cartesian = True
		else:
			self.is_selective_dynamic = False
			self.is_cartesian = False
		# Readin the coordinates of each atom until get a blank line or the end of the file
		line = file.readline()
		self.atom_coordinates = []
		while len(line.strip()) != 0:
			coordinate = [eval(i) for i in line.split()[0:3]]
			self.atom_coordinates.append(coordinate)
			line = file.readline()
		file.close()

	#process coordinates
	def cart2dir(self):
		if self.is_cartesian:
			self.is_cartesian = False
			lat = np.array(self.lat)
			new_coordinates = []
			for c in self.atom_coordinates:
				c = np.array(c)
				new_coordinates.append(list(np.linalg.inv(lat) @ c * self.scaling))
			self.atom_coordinates = new_coordinates

	def dir2cart(self):
		if not self.is_cartesian:
			self.is_cartesian = True
			lat = np.array(self.lat)
			new_coordinates = []
			for c in self.atom_coordinates:
				c = np.array(c)
				new_coordinates.append(list(lat @ c / self.scaling))
				# new_coordinates.append([sum(c[i]*l[j]/self.scaling for i, l in enumerate(self.lat)) \
				# 						for j in range(3)])
			self.atom_coordinates = new_coordinates

	def print(self, show_number=False, show_atom=True, pos_type='direct'):
		'''
		Parameters:
		show_number: Control whether number each line or not. Default value is False.
		show_atom:   Control whether print the atom species or not. Default value is True.
		pos_type:    Choose which coordinates to print.
		'''
		import bisect
		idx_range = [sum(self.atom_num[:i+1])for i in range(len(self.atom_num))]

		# Output atom coordinates type
		if pos_type == 'direct':
			if not self.is_cartesian:
				atom_coordinates = self.atom_coordinates
			else:
				self.cart2dir()
				atom_coordinates = self.atom_coordinates
		elif pos_type == 'cartesian':
			if self.is_cartesian:
				atom_coordinates = self.atom_coordinates
			else:
				self.dir2cart()
				atom_coordinates = self.atom_coordinates
		else:
			raise ValueError('ERROR POS_TYPE!')
			
		for i, c in enumerate(atom_coordinates):
			# Get c atom species
			atom_name_id = bisect.bisect_left(idx_range, i+1)
			atom_name = self.atom_species[atom_name_id]
			if show_number:
				if show_atom:
					print(f'{i+1:<4}{atom_name:4}{c[0]:14.7f}{c[1]:14.7f}{c[2]:14.7f}')
				else:
					print(f'{i+1:<4}{c[0]:14.7f}{c[1]:14.7f}{c[2]:14.7f}')
			else:
				if show_atom:
					print(f'{atom_name:4}{c[0]:14.7f}{c[1]:14.7f}{c[2]:14.7f}')
				else:
					print(f'{c[0]:14.7f}{c[1]:14.7f}{c[2]:14.7f}')

@click.command()
@click.option('-f', '--file', default='./POSCAR', help='POSCAR File')
@click.option('-n', '--number', is_flag=True, help='Show the number of atom')
@click.option('-a', '--atom', is_flag=True, help='Show the species of atom')
@click.option('-d', '--direct', 'pos_type', flag_value='direct', help='Choose Direct coordinates to print.', default=True)
@click.option('-c', '--cartesian', 'pos_type', flag_value='cartesian', help='Choose Cartesian coordinates to print.')
def output(file, number, atom, pos_type):
	'''
	Parameters:
	number: Control whether number each line or not.
	atom: Control whether print the atom species or not.
	pos_type: Choose which coordinates to print.
	'''
	s = POSCAR(file)
	s.print(show_number=number, show_atom=atom, pos_type=pos_type)

if __name__ == "__main__":
	# Test Code
	# s = POSCAR('./test/POSCAR')
	# s.dir2cart()
	# s.cart2dir()

	output()