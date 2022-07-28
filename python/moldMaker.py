from private import path #The full path to the library directory directory
from PIL import Image
import numpy as np

#This file makes it easier to make the molds by using an existing image, and assigning its 9 shades (and 0,0,0,0) a number

originalShades = [[0,0,0,0],[3,26,16,255], [7,36,17,255], [17,56,23,255], [37,82,37,255], [67,105,47,255], [121,156,70,255], [152,179,80,255], [186,196,88,255], [235,224,106,255]]
materialPath = path + 'RP/textures/items/metals/pures/uranium/uranium_'#Path to selected material (Used material_ at the end to complement the following part)

for i in ['raw']:#Write molds to do P.D. the name of the mold has to match an existing image in the 'materialPath' (I complement this by putting the path to the material plus the start of all the files in it which is the material and a '_')
    moldIMG= np.array(Image.open(materialPath+i+'.png')).tolist() #Find the base texture or the mold by name (the image's name has to be the same as the canvas' name)
    newMold= []
    for y in range(16):
        newMold.append([])
        for x in range(16):
            for shade in range(10): #Check if that pixel is in the range of shades
                if moldIMG[y][x] == originalShades[shade]:#Check if the pixel in that x y is in the shades 
                    newMold[y].append(shade) #Assign a number to the pixel depending on the shade
                    break
                elif shade == 9:
                    newMold[y].append(0) #If its not on the shades take it as nothing
                    #print(moldIMG[y][x])  #In case a pixel RGBA value is not in your shades and you cant find what it is

    with open(path+'python/newMolds.txt', 'a') as opnr:
        opnr.write( "\n"+ f'"{i}:: {newMold}'.replace("[", "\n[").replace("\n[\n[", "[\n[") ) #Save mold
