from private import path
from PIL import Image
import numpy as np

originalShades = [[255,255,255,0],[3,26,16,255], [7,36,17,255], [17,56,23,255], [37,82,37,255], [67,105,47,255], [121,156,70,255], [152,179,80,255], [186,196,88,255], [235,224,106,255]]
metalPath = path + 'RP/textures/items/metals/pures/uranium/'#Path to selected material

for i in ['dirty']:#Write toDos
    moldIMG= np.array(Image.open(metalPath+i+'.png')).tolist() #Find the base texture or the mold by name (the image's name has to be the same as the canvas' name)
    newMold= []
    for y in range(16):
        newMold.append([])
        for x in range(16):
            for shade in range(10):
                if moldIMG[y][x] == originalShades[shade]:#Check if the cikir in that x y is in the shades 
                    newMold[y].append(shade)
                    break
                elif shade == 9:
                    newMold[y].append(0)
                    #print(moldIMG[y][x])

    with open(path+'newMolds.py', 'a') as opnr:
        opnr.write( "\n"+ f'{i}= {newMold}'.replace("[", "\n[").replace("\n[\n[", "[\n[") )
