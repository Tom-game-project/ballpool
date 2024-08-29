
import tkinter
import math
from typing import Generator
import random

from PIL import Image, ImageDraw, ImageFont
import cv2

import os

class vector2D:
    """
    ## 簡易的なベクトル計算用モジュール
    python```
v = vector2D(1, 1)
print(
    v*vector2D(-1, 1),
    2*v*2+v,
    v+vector2D(1, 2),
    v-vector2D(1, 2),
)
    ```
    """

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
        return pow(self._x,2)+pow(self._y,2)

    def __abs__(self):
        return math.sqrt(pow(self._x,2)+pow(self._y,2))

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
            """
            内積の場合
            戻り値:int
            """
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            """
            ベクトルの掛け算
            """
            return vector2D(self.x*other, self.y*other)

    def __rmul__(self, other):
        if type(other) is vector2D:
            """
            内積の場合
            戻り値:int
            """
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            """
            ベクトルの掛け算
            """
            return vector2D(self.x*other, self.y*other)

    def __truediv__(self, other) -> "vector2D":
        if (type(other) is int) or (type(other) is float):
            return vector2D(self.x/other, self.y/other)
        else:
            raise BaseException("型が正しくありません")

    def __repr__(self) -> str:
        return f"vector2D({self.x},{self.y})"


class mol:

    def __init__(self,x,y,r,sx,sy,m,color="blue") -> None:
        """
        引数 : x,y,r,sx,sy,m
        """
        self._x = x
        self._y = y
        self._r = r
        self._sx = sx
        self._sy = sy
        self.nextsx = sx
        self.nextsy = sy
        self.m = m
        self._color=color

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
    def color(self):
        return self._color

    @property
    def vector_v(self)->"vector2D":
        """
        速度ベクトル
        """
        return vector2D(self.sx,self.sy)

    @property
    def position_vector(self):
        """
        位置ベクトル
        """
        return vector2D(self.x,self.y)

    def touch_with(self,obj:"mol")->bool:
        """
        触れているか否か
        """
        return (self.x-obj.x)**2+(self.y-obj.y)**2 <= (self.r + obj.r)**2

    def n(self,obj)->"vector2D":
        """
        obj:mol|wall
        法線ベクトル
        """
        if type(obj) is mol:
            return vector2D(self.x,self.y) - vector2D(obj.x,obj.y)
        elif type(obj) is wall:
            o:vector2D = vector2D(self.x,self.y)
            w12 = obj.p2-obj.p1
            ao = o-obj.p1
            a = w12*ao/w12.abspow2
            n = ao-a*w12
            return n
        else:
            raise BaseException("型エラー")

    def inner_product(self,obj:"mol")->float:
        return (-1*vector2D(self.sx,self.sy))*self.n(obj)

    def set_next_v(self,nextv:"vector2D"):
        """
        次の速さの保存
        """
        self.nextsx = nextv.x
        self.nextsy = nextv.y

    def change_v(self):
        """
        次の速さに変更
        """
        self._sx = self.nextsx
        self._sy = self.nextsy

    def change_position(self):
        """
        座標の変更
        """
        self._x += self.sx
        self._y += self.sy

    def position_corection(self,dp:"vector2D"):
        self._x+=dp.x
        self._y+=dp.y


class wall:

    def __init__(self,x1,y1,x2,y2):
        self._p1:vector2D = vector2D(x1,y1)
        self._p2:vector2D = vector2D(x2,y2)

    @property
    def p1(self)->"vector2D":
        return self._p1

    @property
    def p2(self)->"vector2D":
        return self._p2


class mols:

    def __init__(self,wall_e=1,mol_e=1) -> None:
        self.mols_list : list[mol] = []
        self.walls_list:list[wall] = []
        self.e = mol_e
        self.wall_e = wall_e

    def add_mol(self,mol:"mol") -> None:
        self.mols_list.append(mol)

    def add_wall(self,wall:"wall")->None:
        self.walls_list.append(wall)

    def touch_list(self)->Generator:
        back_number_checker:list=[1 for i in self.mols_list]
        for i,j in enumerate(self.mols_list[0:len(self.mols_list)]):
            if back_number_checker[i]:
                for k,l in enumerate(self.mols_list[i+1:]):
                    if j.touch_with(l):
                        back_number_checker[i+k+1]=0
                        yield j,l

    def touch_list_wall(self)->Generator:
        """
        端の方で触れたなら False
        真ん中の方で触れたなら True
        """
        for i in self.mols_list:
            for j in self.walls_list:
                n=i.n(j)
                if n.abspow2<=i.r**2:
                    yield i,j,n
                    break

    def pair_next_v(self,mol1:"mol",mol2:"mol")->tuple[vector2D,vector2D]:
        v1:vector2D=vector2D(mol1.sx, mol1.sy)
        v2:vector2D=vector2D(mol2.sx, mol2.sy)
        n1 = mol1.n(mol2)
        n2 = mol2.n(mol1)
        a = (-1*v1)*n1/n1.abspow2
        b = (-1*v2)*n2/n2.abspow2
        v1x: vector2D = -1*a*n1
        v2x: vector2D = -1*b*n2#-----------------------------------------------------------------------------------------
        k = (mol1.m*v1x+mol2.m*v2x)/(mol1.m+mol2.m)
        l = (v2x-v1x)/(self.e*(mol1.m+mol2.m))
        v1xd:vector2D = k+mol2.m*l
        v2xd:vector2D = k-mol1.m*l
        v1d = v1+a*n1+v1xd
        v2d = v2+b*n2+v2xd
        return v1d,v2d

    def pair_next_v_2(self,mol1:"mol",mol2:"mol"):
        """
        pair_next_vの改善版
        """
        v1: vector2D = vector2D(mol1.sx, mol1.sy)
        v2: vector2D = vector2D(mol2.sx, mol2.sy)
        n1 = mol1.n(mol2)
        n2 = mol2.n(mol1)
        a = (-1*v1)*n1/n1.abspow2
        b = (-1*v2)*n2/n2.abspow2
        v1x: vector2D = -1*a*n1
        v2x: vector2D = -1*b*n2
        v1xd: vector2D = ((1+self.e)*mol2.m*v2x+(mol1.m-self.e*mol2.m)*v1x)/(mol1.m+mol2.m)
        v2xd: vector2D = ((1+self.e)*mol1.m*v1x+(mol2.m-self.e*mol1.m)*v2x)/(mol1.m+mol2.m)
        v1d = v1+a*n1+v1xd
        v2d = v2+b*n2+v2xd
        return v1d, v2d

    def pair_position_corection(self,mol1:"mol",mol2:"mol")->"vector2D":
        """
        座標を補正する
        使用条件:molとの接触
        """
        p1:vector2D = mol1.position_vector
        p2:vector2D = mol2.position_vector
        p12:vector2D = p2-p1
        dp: vector2D = ((-1*(mol1.r+mol2.r-abs(p12)))/(2*abs(p12)))*p12
        mol1.position_corection(dp)
        mol2.position_corection(-1*dp)

    def pair_position_corection_wall(self,mol:"mol",wall:"wall",n:"vector2D"):
        """
        壁との衝突の座標補正
        使用条件:wallとの接触
        """
        an = abs(n)
        dp:vector2D =((mol.r-an)/an)*n 
        mol.position_corection(dp)
        #********************************************************************************************************************

    def wall_next_v(self,mol1:"mol",wall1:"wall",n:"vector2D")->"vector2D":
        molv=mol1.vector_v
        a = (-1*molv)*n/n.abspow2
        nextv:vector2D = molv+(1+self.wall_e)*a*n
        return nextv

    def calc(self):
        for i in self.touch_list():
            """
            次の速さの決定と
            次の速さの設定
            """
            self.pair_position_corection(*i)
            v1d,v2d = self.pair_next_v_2(*i)
            i[0].set_next_v(v1d)
            i[1].set_next_v(v2d)
        for i in self.touch_list_wall():
            """
            壁との衝突による速さの変更
            """
            self.pair_position_corection_wall(*i)
            nextv:vector2D=self.wall_next_v(*i)
            i[0].set_next_v(nextv)
        for i in self.mols_list:
            """
            速さの一括変更
            """
            i.change_v()

    def change(self):
        """
        座標の変更を行う
        """
        for i in self.mols_list:
            i.change_position()

    def __getitem__(self,obj):
        return self.mols_list[obj]


class GasBox(tkinter.Canvas):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,kwargs)

    def delete_all(self):
        self.delete("all")

    def stamp(self,x,y,r,color="black"):
        self.create_oval(x-r,y-r,x+r,y+r,fill=color)

    def mol_stamp(self,mol:"mol"):
        """
        mol object を代入すると自動で描画します
        """
        self.stamp(mol.x,mol.y,mol.r,color=mol.color)


class GasBox_video:

    def __init__(self,width=600,height=600,color=(0,0,0),image_folder="",repeat=10) -> None:
        self.folder:str=image_folder
        self.width:int=width
        self.height:int = height
        self.color=color
        self.repeat=repeat

    def draw_mols(self,mols:"mols",i):
        image = Image.new("RGB", (self.width, self.height), self.color)
        for j in mols:
            dr = ImageDraw.Draw(image)
            dr.ellipse((j.x-j.r,j.y-j.r,j.x+j.r,j.y+j.r),fill=j.color)
        filename = os.path.join(self.folder,str(i).zfill(4))  # 右寄せ0詰めで連番のファイル名を作成
        image.save(filename+'.png', quality=95)

    def calc(self,mols:"mols"):
        for i in range(self.repeat):
            mols.calc()
            mols.change()
            self.draw_mols(mols,i)

    def create_video(self,folder="video"):
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(f'{folder}\\movie.mp4', fourcc, 20.0, (self.width,self.height))
        for i in range(self.repeat):
            filename = f"{self.folder}\\"+str(i).zfill(4)+'.png'  # 読み出すpngファイル名の設定
            img = cv2.imread(filename)  # pngファイル読み出し
            video.write(img)  # 動画の生成

    def delete_image_files(self):
        for i in os.listdir(self.folder):
            os.remove(os.path.join(self.folder,i))

