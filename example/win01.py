from ballpool.real_gas import GasBox, mols, wall, mol
import random
import math
import tkinter

def random_direction(a=1):
    r = random.random()
    d=r*2*math.pi
    return a * math.cos(d),a * math.sin(d)

def loop():
    canvas.delete("all")
    Mols.calc()
    Mols.change()
    for i in Mols:
        canvas.mol_stamp(i)
    for i in Mols.walls_list:
        canvas.wall_stamp(i)
    canvas.after(10, loop)

def set_rect_wall_box(x1,y1,x2,y2):
    Mols.add_wall(
        wall(x1, y1, x1, y2)
    )
    Mols.add_wall(
        wall(x1, y2, x2, y2)
    )
    Mols.add_wall(
        wall(x2, y2, x2, y1)
    )
    Mols.add_wall(
        wall(x2, y1, x1, y1)
    )

def set_triangle_formation(x:int, y:int, r:int, d:int, side:int) -> None:
    sx = x
    sy = y
    for i in range(side):
        for j in range(i + 1):
            Mols.add_mol(mol(sx + j * (2 * r + d), sy, r, 0, 0, 10, color = "red"))
        sx -= 0.5 * (2 * r + d)
        sy += (math.sqrt(3) / 2) * (2 * r + d)

root = tkinter.Tk()
root.title("real gas")

canvas = GasBox(root, width = 600, height = 600, bg = "white")
canvas.pack()

#canvas.after(0,loop)
Mols = mols(mol_e = 1, wall_e = 1)
# setting walls
set_rect_wall_box(30, 30, 400, 400)

for i in range(3):
    for j in range(3):
        Mols.add_mol(
            mol(i * 40 + 150, j * 40 + 200, 10, *(random_direction(a = 3)), 1, color = "#f403fc")
        )

canvas.after(0, loop)
root.mainloop()