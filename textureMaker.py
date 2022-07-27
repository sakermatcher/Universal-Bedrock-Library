from metalMolds import metal
from gemMolds import gem
import numpy as np
from PIL import Image

def hex_to_rgb(values):
    values= values.split('#')
    final=[]
    for h in values:
        final.append(list(int(h[i:i+2], 16) for i in (0, 2, 4)))
    for i in range(len(final)):
        final[i].append(255)

    return final

pallete =  hex_to_rgb("deddf6#c6c3da#ada9be#958ea2#7c7486#645a69#4b404d#332531#1a0b15") #9 colors, darker to lighter
name='lithium'
matType=metal

for key in matType.keys():
    for y in range(16):
        for x in range(16):