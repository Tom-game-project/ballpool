from mol_simulation.mol import GasBox_video
from mol_simulation.real_gas import mols, wall, mol

canvas = GasBox_video(width=600, height=600,image_folder="img",repeat=1000)
canvas.delete_image_files()

Mols = mols(mol_e=1)
# setting walls
Mols.add_wall(
    wall(0, 0, 0, 600)
)
Mols.add_wall(
    wall(0, 600, 600, 600)
)
Mols.add_wall(
    wall(600, 600, 600, 0)
)
Mols.add_wall(
    wall(600, 0, 0, 0)
)

for i in range(18):
    for j in range(7):
        Mols.add_mol(
            mol(i*30+60, j*30+60, 10, 0, 0, 1, color="#f403fc")
        )
Mols.add_mol(
    mol(250, 450, 70, 0, -8, 7, color="#0bfc03")
)

Mols.add_mol(
    mol(450, 450, 70, 0, -8, 7, color="#0bfc03")
)

canvas.calc(Mols)
canvas.create_video()