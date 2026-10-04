"""Make a deuterated topology: change the mass of the amide H (atom 8, NME residue) to 2.014.

Usage:  python make_NMA_D.py NMA.prmtop NMA_D.prmtop

Note: ParmEd's command-line interpreter did NOT have a `changeMass` command here;
it printed "command not recognized" and still wrote an unchanged file ("Done!").
Using the Python API and printing before/after avoids that silent failure.
"""
import sys
import parmed as pmd

src, dst = sys.argv[1], sys.argv[2]
parm = pmd.load_file(src)
atom = parm.atoms[7]            # 0-based index -> atom number 8
assert atom.name == "H" and abs(atom.mass - 1.008) < 1e-3, "unexpected atom; check numbering"
print("before:", atom.name, atom.mass)
atom.mass = 2.014
print("after: ", atom.name, atom.mass)
parm.save(dst, overwrite=True)
