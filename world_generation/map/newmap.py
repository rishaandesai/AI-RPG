import numpy as np
import opensimplex
import time
import random

def hex_to_rgb(h):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def make_ansi(fg_hex,bg_hex):
    fr,fg_,fb=hex_to_rgb(fg_hex)
    s=f"\033[38;2;{fr};{fg_};{fb}m"
    if bg_hex!="None":
        br,bg__,bb=hex_to_rgb(bg_hex)
        s+=f"\033[48;2;{br};{bg__};{bb}m"
    return s

color_map={
    "p":make_ansi("#2AC42E","None"),
    "h":make_ansi("#2ED332","None"),
    "v":make_ansi("#31E134","None"),
    "f":make_ansi("#27A828","None"),
    "F":make_ansi("#27AA29","None"),
    "J":make_ansi("#25A024","None"),
    "y":make_ansi("#DAD91B","None"),
    "Y":make_ansi("#FBFA1E","None"),
    "b":make_ansi("#F7F61F","None"),
    "d":make_ansi("#CBCA1B","None"),
    "c":make_ansi("#4C4C4C","None"),
    "C":make_ansi("#4C4C4C","None"),
    "s":make_ansi("#FFFFFF","None"),
    "r":make_ansi("#010080","None"),
    "l":make_ansi("#010081","None"),
    "w":make_ansi("#010080","None"),
    "R":make_ansi("#E251D9","None"),
    "L":make_ansi("#E43332","None"),
    "^m":make_ansi("#8D8D20","None"),
    "^s":make_ansi("#FFFFFF","None"),
    "~s":make_ansi("#FFFFFF","#027D7E"),
    "~d":make_ansi("#FFFFFF","#01007C"),
    "/":make_ansi("#7F7E1C","None"),
    "/w":make_ansi("#525252","None"),
    "?":make_ansi("#FFFFFF","None"),
    "#":make_ansi("#FFFFFF","None"),
    "!":make_ansi("#FFFFFF","None"),
    "%":make_ansi("#FFFFFF","None"),
    "=":make_ansi("#05A5A6","None")
}

class Tile:
    def __init__(self,char,fgcode):
        self.char=char
        self.fgcode=fgcode

class Worldmap:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.continentmap=np.zeros((height,width),dtype=np.float32)
        self.subcontinent=np.zeros((height,width),dtype=np.float32)
        self.detailmap=np.zeros((height,width),dtype=np.float32)
        self.tempmap=np.zeros((height,width),dtype=np.float32)
        self.moistmap=np.zeros((height,width),dtype=np.float32)
        self.tiles=[[Tile(' ',"\033[0m") for _ in range(width)] for __ in range(height)]
        self.seed=None

    def noise2d(self,x,y,scale,ox=0,oy=0):
        return opensimplex.noise2(scale*(x+ox),scale*(y+oy))/2+0.5

    def gen_worldmaps(self,seed=None):
        if seed is None:
            seed=time.time_ns()
        self.seed=seed
        opensimplex.seed(seed)
        for j in range(self.height):
            for i in range(self.width):
                nx=(i/self.width)
                ny=(j/self.height)
                self.continentmap[j,i]=self.noise2d(nx,ny,0.8,1.7,-2.3)
                self.subcontinent[j,i]=self.noise2d(nx,ny,2.0,-3.1,1.1)
                self.detailmap[j,i]=self.noise2d(nx,ny,6.0,5.7,2.3)
                lat_factor=1-abs((j/self.height)-0.5)*2
                self.tempmap[j,i]=(self.noise2d(nx,ny,0.9,2,2)*0.7+lat_factor*0.3)
                self.moistmap[j,i]=self.noise2d(nx,ny,1.1,-2,5)
        for j in range(self.height):
            for i in range(self.width):
                c=self.continentmap[j,i]*0.6+self.subcontinent[j,i]*0.3+self.detailmap[j,i]*0.1
                d=((i/self.width-0.5)**2+(j/self.height-0.5)**2)**0.5
                e=1-d
                if e<0: e=0
                c*=e
                self.continentmap[j,i]=c

    def place_rivers(self,num=15):
        for _ in range(num):
            x=random.randint(0,self.width-1)
            y=random.randint(0,self.height-1)
            if self.continentmap[y,x]<0.55: continue
            length=random.randint(self.width,self.width*2)
            for __ in range(length):
                self.continentmap[y,x]=min(self.continentmap[y,x],0.27)
                mv=random.choice(['up','down','left','right'])
                if mv=='up' and y>0: y-=1
                elif mv=='down' and y<self.height-1: y+=1
                elif mv=='left' and x>0: x-=1
                elif mv=='right' and x<self.width-1: x+=1

    def classify_tile(self,h,t,m):
        if h<0.02: return Tile('~',color_map["~d"])
        if h<0.07: return Tile('~',color_map["~s"])
        if h<0.1: return Tile('b',color_map["b"])
        if h<0.2: return Tile('y',color_map["y"])
        if h<0.25: return Tile('c',color_map["c"])
        if h<0.3: return Tile('r',color_map["r"])
        if h<0.33: return Tile('l',color_map["l"])
        if h<0.35: return Tile('w',color_map["w"])
        if h>0.97 and t<0.35: return Tile('s',color_map["s"])
        if h>0.9 and t>0.7: return Tile('L',color_map["L"])
        if h>0.88 and t<0.5: return Tile('^',color_map["^s"])
        if h>0.8: return Tile('^',color_map["^m"])
        if t>0.8 and m<0.2: return Tile('d',color_map["d"])
        if t<0.2 and h>0.4: return Tile('s',color_map["s"])
        if m>0.9 and h>0.3: return Tile('Y',color_map["Y"])
        if m>0.8: return Tile('J',color_map["J"])
        if m>0.6: return Tile('F',color_map["F"])
        if m>0.4: return Tile('f',color_map["f"])
        if h>0.4 and random.random()<0.2: return Tile('h',color_map["h"])
        if h<0.4 and random.random()<0.2: return Tile('v',color_map["v"])
        return Tile('p',color_map["p"])

    def map_tiles(self):
        for j in range(self.height):
            for i in range(self.width):
                h=self.continentmap[j,i]
                t=self.tempmap[j,i]
                m=self.moistmap[j,i]
                self.tiles[j][i]=self.classify_tile(h,t,m)

    def place_roads(self,num=6):
        for _ in range(num):
            x1=random.randint(0,self.width-1)
            y1=random.randint(0,self.height-1)
            x2=random.randint(0,self.width-1)
            y2=random.randint(0,self.height-1)
            steps=max(abs(x2-x1),abs(y2-y1))
            dx=(x2-x1)/steps if steps>0 else 0
            dy=(y2-y1)/steps if steps>0 else 0
            cx=float(x1)
            cy=float(y1)
            for __ in range(steps):
                ix=int(round(cx))
                iy=int(round(cy))
                if 0<=ix<self.width and 0<=iy<self.height:
                    c=self.tiles[iy][ix].char
                    if c in ['/','-','\\','|']: self.tiles[iy][ix]=Tile(c,color_map["/"])
                    else: self.tiles[iy][ix]=Tile('/',color_map["/"])
                cx+=dx
                cy+=dy

    def place_walls_cliffs(self,num=4):
        for _ in range(num):
            x1=random.randint(0,self.width-1)
            y1=random.randint(0,self.height-1)
            x2=random.randint(0,self.width-1)
            y2=random.randint(0,self.height-1)
            steps=max(abs(x2-x1),abs(y2-y1))
            dx=(x2-x1)/steps if steps>0 else 0
            dy=(y2-y1)/steps if steps>0 else 0
            cx=float(x1)
            cy=float(y1)
            for __ in range(steps):
                ix=int(round(cx))
                iy=int(round(cy))
                if 0<=ix<self.width and 0<=iy<self.height:
                    c=self.tiles[iy][ix].char
                    if c in ['/','-','\\','|']: self.tiles[iy][ix]=Tile(c,color_map["/w"])
                    else: self.tiles[iy][ix]=Tile('/',color_map["/w"])
                cx+=dx
                cy+=dy

    def place_cities(self,num=20):
        for _ in range(num):
            x=random.randint(0,self.width-1)
            y=random.randint(0,self.height-1)
            self.tiles[y][x]=Tile('=',color_map["="])

    def place_structs(self,num=30):
        picks=['?','!','#','%']
        for _ in range(num):
            x=random.randint(0,self.width-1)
            y=random.randint(0,self.height-1)
            c=random.choice(picks)
            self.tiles[y][x]=Tile(c,color_map[c])

    def render(self):
        for j in range(self.height):
            row=''
            for i in range(self.width):
                row+=self.tiles[j][i].fgcode+self.tiles[j][i].char+"\033[0m"
            print(row)

def generate_world(width=400,height=120):
    wm=Worldmap(width,height)
    wm.gen_worldmaps()
    wm.place_rivers()
    wm.map_tiles()
    wm.place_roads()
    wm.place_walls_cliffs()
    wm.place_cities()
    wm.place_structs()
    wm.render()

if __name__=="__main__":
    generate_world()