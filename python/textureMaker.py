from metalMolds import metal
from gemMolds import gem 
import numpy as np #pip install numpy
from PIL import Image
from private import path #The full path to the library directory directory

def hex_to_rgb(values):#Convert Hex values that are cramped together in a str separated by a hashtag to RGBA tuples
    values= values.split('#')
    final=[(0,0,0,0)]
    prefinal = []
    for h in values:
        prefinal.append(list(int(h[i:i+2], 16) for i in (0, 2, 4)))
        prefinal[-1].append(255)
    for i in range(len(prefinal)):
        final.append(tuple(prefinal[i]))

    return final



#User Input Here:
pallete =  hex_to_rgb("0A0715#181435#1D2557#33246D#9D348F#B63DB2#B24DC4#D98EC3#D6B0E5") #9 colors, darker to lighter I use https://www.toptal.com/designers/colourcode/freebuild-color-builder# to get the palletes
name='lithium' #name of the material (make a folder were your path is pointing with the name of the material to dump the textures)
matType=metal #metal or gem




for key in matType.keys():#Go thru every type of item that that material can have
    newTexture = [] #List containing the newly made texture
    for y in range(16):
        newTexture.append([])
        for x in range(16):
            if key != 'dirty_dust': #The dirty dust texture has to have its brightness reduced to a 80% so its in a separate if
                newTexture[y].append(pallete[matType[key][y][x]]) #Add the pallete color that represents the number in the mold
            else:
                newRGBa = [] #Make a new RGBa with brightness reduced
                for i in range (3): #Go thru RGB
                    newRGBa.append (int(pallete[matType[key][y][x]][i]*0.8)) #Put the brightness of each R, G, B to a 80%
                
                newRGBa.append(pallete[matType[key][y][x]][3])#Append the alpha channel
                newRGBa= tuple(newRGBa) #Make it a tuple so that its compatible
                newTexture[y].append(newRGBa) #Add it to the new texture

    newTextureResult = Image.fromarray(np.uint8(np.array(newTexture))) #Convert the list with RGBA values to an np.array and later to an image
    newTextureResult.save(f'{path}{name}/{name}_{key}.png') #Save the image