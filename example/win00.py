import random
import tkinter
import math

from mol_simulation.mol import GasBox,mols,wall,mol

def random_direction(a=1):
    r = random.random()
    d = r*2*math.pi
    return a*math.cos(d), a*math.sin(d)

root = tkinter.Tk()
root.title("実在気体")
def loop():
    canvas.delete("all")
    Mols.calc()
    Mols.change()
    for i in Mols:
        canvas.mol_stamp(i)
    canvas.after(10, loop)

canvas = GasBox(root, width=600, height=600)
canvas.pack()
Mols = mols(mol_e=0.99)
Mols.add_wall(wall(0, 0, 0, 600))
Mols.add_wall(wall(0, 600, 600, 600))
Mols.add_wall(wall(600, 600, 600, 0))
Mols.add_wall(wall(600, 0, 0, 0))
for i in range(4):
    for j in range(4):
        Mols.add_mol(mol(i*130+60, j*130+60, 30, *random_direction(a=2), 1, color = ["#ff0000","#00ff00","#0000ff"][(i + j) % 3]))
canvas.after(0, loop)
root.mainloop()

print("hello")