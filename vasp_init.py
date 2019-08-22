#!/bin/python3

import os

def incar(system='vasp', istart=0, icharg=2, soc=True, w90=False):
    incar_string = '''SYSTEM = {0}

# Startparameter for this run:
  PREC   = Accurate
  ISTART = {1:1d}
  ICHARG = {2:1d}
  LREAL  = .FALSE.

# Ionic Relaxation
  # IBRION = -1
  # ISIF   = 3
  # NSW    = 0
  # EDIFFG = -0.0001
  # POTIM  = 0.1

# Electronic Relaxation   
  EDIFF  = 1.0E-06
  ENCUT  = 260 eV
  ALGO   = Fast
  NELMIN = 4
  NELM   = 200
  # EMIN   = -15
  # EMAX   = 15
  # NEDOS  = 3001

# DOS related values 
  ISMEAR = 0
  SIGMA  = 0.05

# Field Calculation
  # EFIELD = 0.1
  # LDIPOL = .TRUE.
  # IDIPOL = 3
  # DIPOL  = 0.5 0.5 0.1374

# Writing items
  LWAVE  = .FALSE.
  LCHARG = .TRUE.
  LVTOT  = .FALSE.

# Speed up parameters
  # NCORE  = 20
  # LPLANE = .TRUE.
  # LSCALU = .FALSE.
  # NSIM   = 4'''
  
    soc_string = '''# SOC
  LORBIT  = 11
  ISPIN   = 2
  MAGMOM  = 4*0 4*0 4*0 8*0 8*0 8*0
  LSORBIT = .TRUE.
  LMAXMIX = 4
  SAXIS   = 0 0 1
  NBANDS  = 160
  ISYM    = 0
  GGA_COMPAT = .FALSE.
  LORBMOM    = .TRUE.'''

    w90_string = '''# Wannier90
  LWANNIER90     = .TRUE.
  LWRITE_MMN_AMN = .TRUE.
  LWRITE_UNK     = .FALSE.'''

    with open('INCAR', 'w') as f:
    	f.writelines(incar_string.format(system, istart, icharg))
    	if soc:
    		f.writelines('\n\n')
    		f.writelines(soc_string)
    	if w90:
    		f.writelines('\n\n')
    		f.writelines(w90_string)

def kpoints(k_type):
    kpoints_string = '''Automatic generation
0
Gamma
12  10   6
0.0  0.0  0.0'''
    band_string = '''WTe2
50   ! 50 grids
Line-mode
reciprocal
   0.0000   0.0000   0.0000   ! G
   0.0000   0.5000   0.0000   ! Y

   0.0000   0.5000   0.0000   ! Y
   0.5000   0.5000   0.0000   ! S

   0.5000   0.5000   0.0000   ! S
   0.5000   0.0000   0.0000   ! X

   0.5000   0.0000   0.0000   ! X
   0.0000   0.0000   0.0000   ! G

   0.0000   0.0000   0.0000   ! G
   0.0000   0.0000   0.5000   ! Z

   0.0000   0.0000   0.5000   ! Z
   0.0000   0.5000   0.5000   ! T

   0.0000   0.5000   0.5000   ! T
   0.5000   0.5000   0.5000   ! R

   0.5000   0.5000   0.5000   ! R
   0.5000   0.0000   0.5000   ! U

   0.5000   0.0000   0.5000   ! U
   0.0000   0.0000   0.5000   ! Z
'''
    with open('KPOINTS', 'w') as f:
    	if k_type == 'kpts':
    		f.writelines(kpoints_string)
    	elif k_type == 'band':
    		f.writelines(band_string)
    	else:
    		raise ValueError(f'Wrong Type of Kpoints: {k_type}')

def run_script(exe=['vasp']):
    run_string = '''#!/bin/bash
#
#SBATCH --job-name=vasp
#SBATCH --output=job_%j.out
#SBATCH --nodes=1
#SBATCH --time=3:00:00
#SBATCH --partition=regular

export I_MPI_FABRICS=shm:ofa

# where is your binary file
'''
    exe_string = '''# VASP Location
# EXE=/software/vasp/vasp.5.4.1/bin/vasp_gam
# EXE=/software/vasp/vasp.5.4.1/bin/vasp_ncl
# EXE=/software/vasp/vasp.5.4.1/bin/vasp_std

# VASP with wannier90 Location
# EXE=/home/enwang/bin/vasp_wannier90/vasp.5.4.1/bin/vasp_gam
# EXE=/home/enwang/bin/vasp_wannier90/vasp.5.4.1/bin/vasp_ncl
# EXE=/home/enwang/bin/vasp_wannier90/vasp.5.4.1/bin/vasp_std

# Wannier90
# EXE=/home/enwang/bin/wannier90/wannier90-3.0.0/wannier90.x
# SYSTEM="wannier90"

# WannierTools
# EXE=/home/enwang/bin/wannier_tools-2.4.1/bin/wt.x'''

# run the job
# mpirun -n 40 -ppn 40 $EXE $SYSTEM
# mpirun -n 40 -ppn 40 $EXE
    
    if not isinstance(exe, list) and not isinstance(exe, tuple):
    	exe = [exe]

    exe_dict = {'vasp'   : '/software/vasp/vasp.5.4.1/bin/vasp_',
                'vaspw90': '/home/enwang/bin/vasp_wannier90/vasp.5.4.1/bin/vasp_',
    			'w90'    : '/home/enwang/bin/wannier90/wannier90-3.0.0/wannier90.x',
    			'wt'     : '/home/enwang/bin/wannier_tools-2.4.1/bin/wt.x'}
    with open('run.script', 'w') as f:
    	f.writelines(run_string)
    	# exe
    	for e in exe:
    		if e == 'w90':
    			f.writelines('# Wannier90\n')
    			f.writelines('EXE={0}\n'.format(exe_dict['w90']))
    		elif e == 'wt':
    			f.writelines('# WannierTools\n')
    			f.writelines('EXE={0}\n'.format(exe_dict['wt']))
    		elif e[:5] == 'vasp_':
    			f.writelines('# VASP\n')
    			f.writelines('EXE={0}{1}\n'.format(exe_dict['vasp'], e[-3:]))
    		elif e[:8] == 'vaspw90_':
    			f.writelines('# VASP with wannier90\n')
    			f.writelines('EXE={0}{1}\n'.format(exe_dict['vaspw90'], e[-3:]))
    		elif e == 'all':
    			f.writelines(exe_string)
    		else:
    			raise ValueError(f'{e} is not in executable programs list.')
    	# mpirun
    	f.writelines('\n# run the job\n')
    	if 'w90' in exe:
    		f.writelines('mpirun -n 40 -ppn 40 $EXE $SYSTEM')
    	else:
    		f.writelines('mpirun -n 40 -ppn 40 $EXE')

def w90in(nw, nb):
    win_string = '''num_wann  = {0:d}
num_bands = {1:d}

begin projections
W: l=0;l=2
Te: l=1
end projections

#dis_win_max     =  16.0
#dis_win_min     = -1.0
#dis_froz_max    =  8.0
#dis_froz_min    =  6.0

#dis_num_iter    =  4000
#dis_mix_ratio   =  0.9d0
#num_iter          = 800
#num_print_cycles  = 10

#band structure plot
#restart     = plot
#bands_plot  = .true.
#begin kpoint_path
#G   0.0000   0.0000   0.0000    Y   0.0000   0.5000   0.0000
#Y   0.0000   0.5000   0.0000    S   0.5000   0.5000   0.0000
#S   0.5000   0.5000   0.0000    X   0.5000   0.0000   0.0000
#X   0.5000   0.0000   0.0000    G   0.0000   0.0000   0.0000
#G   0.0000   0.0000   0.0000    Z   0.0000   0.0000   0.5000
#Z   0.0000   0.0000   0.5000    T   0.0000   0.5000   0.5000
#T   0.0000   0.5000   0.5000    R   0.5000   0.5000   0.5000
#R   0.5000   0.5000   0.5000    U   0.5000   0.0000   0.5000
#U   0.5000   0.0000   0.5000    Z   0.0000   0.0000   0.5000
#end kpoint_path
#bands_num_points 100
#bands_plot_format gnuplot xmgrace
'''
    with open('wannier90.win', 'w') as f:
    	f.writelines(win_string.format(nw, nb))

def wtin():
    wt_string = '''&TB_FILE
Hrfile = 'wannier90_hr.dat'
Package = 'VASP'             ! obtained from VASP, it could be 'VASP', 'QE', 'Wien2k', 'OpenMx'
/

LATTICE
Angstrom
     3.4770000     0.0000000     0.0000000  ! crystal lattice information
     0.0000000     6.2490001     0.0000000
     0.0000000     0.0000000    14.0179996

ATOM_POSITIONS
12                               ! number of atoms for projectors
Direct                           ! Direct or Cartisen coordinate
W   0.00000000  0.60061996  0.50000000
W   0.50000000  0.39938004  0.00000000
W   0.00000000  0.03980000  0.01522000
W   0.50000000  0.96020001  0.51521998
Te  0.00000000  0.85760997  0.65524999
Te  0.50000000  0.14239001  0.15524996
Te  0.00000000  0.64630999  0.11112000
Te  0.50000000  0.35369001  0.61112000
Te  0.00000000  0.29845000  0.85983001
Te  0.50000000  0.70155000  0.35983001
Te  0.00000000  0.20722000  0.40386999
Te  0.50000000  0.79277996  0.90386999

PROJECTORS
 6 6 6 6 3 3 3 3 3 3 3 3          ! number of projectors
W s dxy dxz dyz dx2-y2 dz2    ! projectors
W s dxy dxz dyz dx2-y2 dz2
W s dxy dxz dyz dx2-y2 dz2
W s dxy dxz dyz dx2-y2 dz2
Te px py pz
Te px py pz
Te px py pz
Te px py pz
Te px py pz
Te px py pz
Te px py pz
Te px py pz

SURFACE            ! See doc for details
 1  0  0
 0  1  0
 0  0  1

&CONTROL
!BulkBand_calc         = T
!BulkFS_calc           = T
!BulkGap_cube_calc     = T
!BulkGap_plane_calc    = T
!WeylChirality_calc    = T
!FindNodes_calc        = T
!SlabBand_calc         = T
!WireBand_calc         = T
!SlabSS_calc           = T
!SlabArc_calc          = T
!SlabQPI_calc          = T
!SlabSpintexture_calc  = T
!Wanniercenter_calc    = T
!BerryCurvature_calc   = T
!EffectiveMass_calc    = T
/

&SYSTEM
!NSLAB = 10              ! for thin film system
!NSLAB1= 4               ! nanowire system
!NSLAB2= 4               ! nanowire system
NumOccupied = 56         ! NumOccupied
SOC = 1                  ! soc
E_FERMI = 7.3139         ! e-fermi
!Bx= 0, By= 0, Bz= 0     ! Bx By Bz
!surf_onsite= 0.0        ! surf_onsite
/

&PARAMETERS
!Eta_Arc = 0.001     ! infinite small value, like brodening
!E_arc = 0.0         ! energy for calculate Fermi Arc
!OmegaNum = 100      ! omega number
!OmegaMin = -0.6     ! energy interval
!OmegaMax =  0.5     ! energy interval
Nk1 = 21            ! number k points  odd number would be better
Nk2 = 21            ! number k points  odd number would be better
Nk3 = 21            ! number k points  odd number would be better
!NP = 1              ! number of principle layers
Gap_threshold = 0.0001 ! threshold for GapCube output
/

KPATH_BULK     ! k point path
9              ! number of k lines only for bulk band
G   0.0000   0.0000   0.0000    Y   0.0000   0.5000   0.0000
Y   0.0000   0.5000   0.0000    S   0.5000   0.5000   0.0000
S   0.5000   0.5000   0.0000    X   0.5000   0.0000   0.0000
X   0.5000   0.0000   0.0000    G   0.0000   0.0000   0.0000
G   0.0000   0.0000   0.0000    Z   0.0000   0.0000   0.5000
Z   0.0000   0.0000   0.5000    T   0.0000   0.5000   0.5000
T   0.0000   0.5000   0.5000    R   0.5000   0.5000   0.5000
R   0.5000   0.5000   0.5000    U   0.5000   0.0000   0.5000
U   0.5000   0.0000   0.5000    Z   0.0000   0.0000   0.5000

!KPATH_SLAB
!2        ! numker of k line for 2D case
!K 0.33 0.67 G 0.0 0.0  ! k path for 2D case
!G 0.0 0.0 M 0.5 0.5

!KPLANE_SLAB
!-0.1 -0.1      ! Original point for 2D k plane
! 0.2  0.0      ! The first vector to define 2D k plane
! 0.0  0.2      ! The second vector to define 2D k plane  for arc plots

!KPLANE_BULK
! 0.12100  0.03000  0.00000   ! Original point for 3D k plane
! 0.00100  0.00000  0.00000   ! The first vector to define 3d k space plane
! 0.00000  0.02000  0.00000   ! The second vector to define 3d k space plane

!KPLANE_BULK
! 0.00  0.00  0.00   ! Original point for 3D k plane
! 0.50  0.00  0.00   ! The first vector to define 3d k space plane
! 0.00  0.50  0.00   ! The second vector to define 3d k space plane

!KCUBE_BULK
!-0.50 -0.50 -0.50   ! Original point for 3D k plane
! 1.00  0.00  0.00   ! The first vector to define 3d k space plane
! 0.00  1.00  0.00   ! The second vector to define 3d k space plane
! 0.00  0.00  1.00   ! The third vector to define 3d k cube

!WEYL_CHIRALITY
!8    ! How many Weyl points
!Cart
!0.002

!EFFECTIVE_MASS      ! optional
!2                   ! The i'th band to be calculated
!0.01                ! k step in unit of (1/Angstrom)
!0.0 0.0 0.0         ! k point where the effective mass calculated.

WANNIER_CENTRES     ! copy from wannier90.wout
Cartesian
'''
    with open('wt.in', 'w') as f:
    	f.writelines(wt_string)
    
if __name__ == '__main__':
    # self-consistent
    incar(system='WTe2', istart=0, icharg=2, soc=True, w90=False)
    kpoints(k_type='kpts')
    run_script(exe='vasp_ncl')
    os.system('chmod +x run.script')
    # bnd
    os.mkdir('bnd')
    os.chdir('./bnd')
    os.system('ln -s ../CHRCAR CHGCAR')
    os.system('cp ../POSCAR ../POTCAR .')
    incar(system='WTe2', istart=0, icharg=11, soc=True, w90=False)
    kpoints(k_type='band')
    run_script(exe='vasp_ncl')
    os.system('chmod +x run.script')
    os.chdir('..')
    # wannier
    os.mkdir('wannier')
    os.chdir('./wannier')
    os.system('ln -s ../CHRCAR CHGCAR')
    os.system('cp ../POSCAR ../POTCAR .')
    incar(system='WTe2', istart=0, icharg=11, soc=True, w90=True)
    kpoints(k_type='kpts')
    w90in(96, 160)
    run_script(exe='vaspw90_ncl')
    os.system('chmod +x run.script')
    # wannier90
    os.mkdir('wannier90')
    os.chdir('./wannier90')
    for file in ['amn', 'eig', 'mmn']:
    	os.system('ln -s ../wannier90.{0} wannier90.{0}'.format(file))
    wtin()
    run_script(exe=['wt', 'w90'])
    os.system('chmod +x run.script')

    os.chdir('../../..')
