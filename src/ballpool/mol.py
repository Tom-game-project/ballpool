import os
from PIL import Image, ImageDraw
import cv2

from ballpool.real_gas import mols

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
            dr.ellipse((j.x - j.r, j.y - j.r, j.x + j.r, j.y + j.r), fill = j.color)
        filename = os.path.join(self.folder,str(i).zfill(4))  # 右寄せ0詰めで連番のファイル名を作成
        image.save(filename+'.png', quality=95)

    def calc(self,mols:"mols"):
        for i in range(self.repeat):
            mols.calc()
            mols.change()
            self.draw_mols(mols,i)

    def create_video(self,folder="video"):
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        
        video = cv2.VideoWriter(
            os.path.join(folder, "movie.mp4"),
            fourcc,
            20.0,
            (self.width,self.height)
        )
        for i in range(self.repeat):
            filename = os.path.join(self.folder,str(i).zfill(4)+'.png') # 読み出すpngファイル名の設定
            # filename = f"{self.folder}\\"+str(i).zfill(4)+'.png'  
            img = cv2.imread(filename)  # pngファイル読み出し
            video.write(img)  # 動画の生成

    def delete_image_files(self):
        for i in os.listdir(self.folder):
            os.remove(os.path.join(self.folder,i))

