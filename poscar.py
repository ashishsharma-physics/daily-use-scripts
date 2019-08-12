#!/usr/bin/env python
# -*- coding: utf-8 -*-

# * POSCAR Output
# * by En Wang, SF10, IOP, CAS (enwang@iphy.ac.cn)

import re

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
		# The number of atom per atomic species
		tmp = file.readline()
		# if line is atomic species name, read next line to get number
		if re.search('[a-zA-Z]', tmp):
			self.atom_num = [eval(i) for i in file.readline().split()]
			self.atom_species = tmp.split()
		else:
			self.num_atom = [eval(i) for i in tmp]
			self.species_atom = [''] * len(self.num_atom)
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
	
	def output(self, is_number=False, is_atom_name=False):
		'''
		Parameters:
		is_number: Control whether number each line or not. Default value is False.
		is_atom_name: Control whether print the atom species or not. Default value is False.
		'''
		import bisect
		idx_range = [sum(self.atom_num[:i+1])for i in range(len(self.atom_num))]
		
		for i, c in enumerate(self.atom_coordinates):
			# Get c atom species
			atom_name_id = bisect.bisect_left(idx_range, i+1)
			atom_name = self.atom_species[atom_name_id]
			if is_number:
				if is_atom_name:
					print(f'{i+1}\t{atom_name}\t{c[0]:.8f}\t{c[1]:.8f}\t{c[2]:.8f}')
				else:
					print(f'{i+1}\t{atom_name}\t{c[0]:.8f}\t{c[1]:.8f}\t{c[2]:.8f}')
			else:
				if is_atom_name:
					print(f'{i+1}\t{atom_name}\t{c[0]:.8f}\t{c[1]:.8f}\t{c[2]:.8f}')
				else:
					print(f'{i+1}\t{atom_name}\t{c[0]:.8f}\t{c[1]:.8f}\t{c[2]:.8f}')

if __name__ == "__main__":
	s = POSCAR('./test/POSCAR')
	s.output(is_atom_name=True, is_number=False)