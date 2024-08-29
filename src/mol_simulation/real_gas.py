
import tkinter
import math
from typing import Generator
import random
class vector2D:

    def __init__(self, x: float, y: float):
        self._x: float = x
        self._y: float = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def abspow2(self):
        return pow(self._x, 2)+pow(self._y, 2)

    def __abs__(self):
        return math.sqrt(pow(self._x, 2)+pow(self._y, 2))

    def __add__(self, other) -> "vector2D":
        if type(other) is vector2D:
            return vector2D(self.x+other.x, self.y+other.y)
        else:
            raise BaseException("vector2D同士で計算してください")

    def __sub__(self, other) -> "vector2D":
        if type(other) is vector2D:
            return vector2D(self.x-other.x, self.y-other.y)
        else:
            raise BaseException("vector2D同士で計算してください")

    def __mul__(self, other):
        if type(other) is vector2D:
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            return vector2D(self.x*other, self.y*other)

    def __rmul__(self, other):
        if type(other) is vector2D:
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            return vector2D(self.x*other, self.y*other)

    def __truediv__(self, other) -> "vector2D":
        if (type(other) is int) or (type(other) is float):
            return vector2D(self.x/other, self.y/other)
        else:
            raise BaseException("型が正しくありません")

    def __repr__(self) -> str:
        return f"vector2D({self.x},{self.y})"

class mol:

    def __init__(self, x, y, r, sx, sy, m, color = "black") -> None:
        self._x = x
        self._y = y
        self._r = r
        self._sx = sx
        self._sy = sy
        self.nextsx = sx
        self.nextsy = sy
        self.m = m
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def r(self):
        return self._r

    @property
    def sx(self):
        return self._sx

    @property
    def sy(self):
        return self._sy

    @property
    def vector_v(self) -> "vector2D":
        return vector2D(self.sx, self.sy)

    @property
    def position_vector(self):
        return vector2D(self.x, self.y)

    @property
    def color(self):
        return self._color

    def touch_with(self, obj: "mol") -> bool:
        return (self.x-obj.x)**2+(self.y-obj.y)**2 <= (self.r + obj.r)**2

    def n(self, obj) -> "vector2D":
        if type(obj) is mol:
            return vector2D(self.x, self.y) - vector2D(obj.x, obj.y)
        elif type(obj) is wall:
            o: vector2D = vector2D(self.x, self.y)
            w12 = obj.p2-obj.p1
            ao = o-obj.p1
            a = w12*ao/w12.abspow2
            n = ao-a*w12
            return n
        else:
            raise BaseException("型エラー")

    def inner_product(self, obj: "mol") -> float:
        return (-1*vector2D(self.sx, self.sy))*self.n(obj)

    def set_next_v(self, nextv: "vector2D"):
        self.nextsx = nextv.x
        self.nextsy = nextv.y

    def change_v(self):
        self._sx = self.nextsx
        self._sy = self.nextsy

    def change_position(self):
        self._x += self.sx
        self._y += self.sy

    def position_corection(self, dp: "vector2D"):
        self._x += dp.x
        self._y += dp.y


class wall:

    def __init__(self, x1, y1, x2, y2):
        self._p1: vector2D = vector2D(x1, y1)
        self._p2: vector2D = vector2D(x2, y2)

    @property
    def p1(self) -> "vector2D":
        return self._p1

    @property
    def p2(self) -> "vector2D":
        return self._p2


class mols:

    def __init__(self, wall_e=1, mol_e=1) -> None:
        self.mols_list: list[mol] = []
        self.walls_list: list[wall] = []
        self.e = mol_e
        self.wall_e = wall_e

    def add_mol(self, mol: "mol") -> None:
        self.mols_list.append(mol)

    def add_wall(self, wall: "wall") -> None:
        self.walls_list.append(wall)

    def touch_list(self) -> Generator:
        back_number_checker: list = [1 for i in self.mols_list]
        for i, j in enumerate(self.mols_list[0:len(self.mols_list)]):
            if back_number_checker[i]:
                for k, l in enumerate(self.mols_list[i+1:]):
                    if j.touch_with(l):
                        back_number_checker[i+k+1] = 0
                        yield j, l

    def touch_list_wall(self) -> Generator:
        for i in self.mols_list:
            for j in self.walls_list:
                n = i.n(j)
                if n.abspow2 <= i.r**2:
                    yield i, j, n
                    break

    def pair_next_v(self, mol1: "mol", mol2: "mol") -> tuple[vector2D, vector2D]:
        v1: vector2D = vector2D(mol1.sx, mol1.sy)
        v2: vector2D = vector2D(mol2.sx, mol2.sy)
        n1 = mol1.n(mol2)
        n2 = mol2.n(mol1)
        a = (-1*v1)*n1/n1.abspow2
        b = (-1*v2)*n2/n2.abspow2
        v1x: vector2D = -1*a*n1
        v2x: vector2D = -1*b*n2
        v1xd: vector2D = ((1+self.e)*mol2.m*v2x + (mol1.m-self.e*mol2.m)*v1x)/(mol1.m+mol2.m)
        v2xd: vector2D = ((1+self.e)*mol1.m*v1x + (mol2.m-self.e*mol1.m)*v2x)/(mol1.m+mol2.m)
        v1d = v1+a*n1+v1xd
        v2d = v2+b*n2+v2xd
        return v1d, v2d

    def pair_position_corection(self, mol1: "mol", mol2: "mol") -> "vector2D":
        p1: vector2D = mol1.position_vector
        p2: vector2D = mol2.position_vector
        p12: vector2D = p2-p1
        dp: vector2D = ((-1*(mol1.r+mol2.r-abs(p12)))/(2*abs(p12)))*p12
        mol1.position_corection(dp)
        mol2.position_corection(-1*dp)

    def pair_position_corection_wall(self, mol: "mol", wall: "wall", n: "vector2D"):
        an = abs(n)
        dp: vector2D = ((mol.r-an)/an)*n
        mol.position_corection(dp)

    def wall_next_v(self, mol1: "mol", wall1: "wall", n: "vector2D") -> "vector2D":
        molv = mol1.vector_v
        a = (-1*molv)*n/n.abspow2
        nextv: vector2D = molv+(1+self.wall_e)*a*n
        return nextv

    def calc(self):
        for i in self.touch_list():
            self.pair_position_corection(*i)
            v1d, v2d = self.pair_next_v(*i)
            i[0].set_next_v(v1d)
            i[1].set_next_v(v2d)
        for i in self.touch_list_wall():
            self.pair_position_corection_wall(*i)
            nextv: vector2D = self.wall_next_v(*i)
            i[0].set_next_v(nextv)
        for i in self.mols_list:
            i.change_v()

    def change(self):
        for i in self.mols_list:
            i.change_position()

    def __getitem__(self, obj):
        return self.mols_list[obj]


class GasBox(tkinter.Canvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)

    def delete_all(self):
        self.delete("all")

    def stamp(self, x, y, r, color="black"):
        self.create_oval(x-r, y-r, x+r, y+r, fill=color)

    def mol_stamp(self, mol_: "mol"):
        self.stamp(mol_.x, mol_.y, mol_.r, color=mol_.color)


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
