# Reproduce Step A: N-H vs N-D in NMA
# one trajectory with one random seed
# Run inside the `amber_env` conda environment with AmberTools.

set -e

echo "=== Step A: build and minimization ==="

# 0. Build NMA system
tleap -f inputs/tleap.in

# 1. Classical MM minimization
sander -O \
  -i inputs/min_classical.in \
  -o min_classical.out \
  -p NMA.prmtop \
  -c NMA.inpcrd \
  -r min_classical.rst

# 2. PM3 QM/MM minimization
sander -O \
  -i inputs/min_qmmm.in \
  -o min_qmmm.out \
  -p NMA.prmtop \
  -c NMA.inpcrd \
  -r min_qmmm.rst

# 3. Generate deuterated topology
python scripts/make_NMA_D.py \
  NMA.prmtop \
  NMA_D.prmtop


echo "=== Experiment 1: single-point H vs D ==="

sander -O \
  -i inputs/sp_pm3.in \
  -o sp_H.out \
  -p NMA.prmtop \
  -c min_qmmm.rst \
  -r sp_H.rst

sander -O \
  -i inputs/sp_pm3.in \
  -o sp_D.out \
  -p NMA_D.prmtop \
  -c min_qmmm.rst \
  -r sp_D.rst


echo "=== Experiment 2: 0.5 ps QM/MM MD, H vs D ==="

sander -O \
  -i inputs/md_pm3_long.in \
  -o md_H_long.out \
  -p NMA.prmtop \
  -c min_qmmm.rst \
  -r md_H_long.rst \
  -x md_H_long.nc

sander -O \
  -i inputs/md_pm3_long.in \
  -o md_D_long.out \
  -p NMA_D.prmtop \
  -c min_qmmm.rst \
  -r md_D_long.rst \
  -x md_D_long.nc


echo "=== Extract N-H / N-D distances ==="

# Atom 7 = amide N
# Atom 8 = amide H/D

cpptraj -p NMA.prmtop << 'CPP'
trajin md_H_long.nc
distance NH @7 @8 out dist_H_long.dat
run
CPP

cpptraj -p NMA_D.prmtop << 'CPP'
trajin md_D_long.nc
distance ND @7 @8 out dist_D_long.dat
run
CPP


echo "=== Fourier analysis ==="

# 0.5 = MD timestep in fs
python scripts/analyze_nh_spectrum.py \
  dist_H_long.dat \
  dist_D_long.dat \
  0.5

echo "=== Step A completed ==="