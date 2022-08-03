import base64
from molds import molds 
import numpy as np #pip install numpy
from PIL import Image
import PySimpleGUI as sg
from io import BytesIO
import os

palletInUse= ['000000', '0f0f0f', '272727', '4a4a4a', '777777', 'a7a7a7', 'd2d2d2', 'f3f3f3', 'ffffff']
newImages={}
lookingAt= 'Mblock'
unReDo={'at':0, 'history':{0:['000000', '0f0f0f', '272727', '4a4a4a', '777777', 'a7a7a7', 'd2d2d2', 'f3f3f3', 'ffffff']}}
matType= 'metal'
path= ''

def pil_base64(image):
  img_buffer = BytesIO()
  image.save(img_buffer, format='PNG')
  byte_data = img_buffer.getvalue()
  base64_str = base64.b64encode(byte_data)
  return base64_str

def hex_rgb(values):#Convert Hex values that are cramped together in a str separated by a hashtag to RGBA tuples
    final=[]
    for h in values:
        final.append(list(int(h[i:i+2], 16) for i in (0, 2, 4)))
        final[-1].append(255)

    return final

def sgHelper(helpWith):
    """
    typeImages, colors
    """
    global unReDo, newImages, palletInUse
    
    if helpWith[0] == 'typeImages':
        x=[[sg.Text('Metal:', justification='center')]]
        y=[[sg.Text('Gem:', justification='center')]]
        
        for i in molds.keys():
            if i[0] == 'M':
                x.append([sg.Button('', key=i, image_size=(36,36), image_data=resizeAndConvert(newImages[i], 2)), sg.Text(i.lstrip('M'))])
            else:
                y.append([sg.Button('', key=i, image_size=(36,36), image_data=resizeAndConvert(newImages[i], 2)), sg.Text(i.lstrip('G'))])

        return [[sg.Column(x, vertical_alignment='top'), sg.VSeparator(), sg.Column(y, vertical_alignment='top')]]

    elif helpWith[0] == 'colors':
        x=[]
        x.append([sg.Text('Darker')])
        for i in range(9):
            x.append([sg.ColorChooserButton('', button_color=('#'+palletInUse[i], '#'+palletInUse[i]), target='color'+str(i), size=(3,1), key=f'buttoncolor{i}'), sg.Input('#'+palletInUse[i], key=f'color{i}', disabled=True, size=(8,2), readonly=True, text_color='#0f0f0f', enable_events=True)])
        
        return x+ [[sg.Text('Lighter')]]

            


def resizeAndConvert(img, multiplier):
    if type(img) != type([]):
        listImg= np.array(img).tolist()
    else:
        listImg= img  
    result= []
    for y in range(len(listImg)):
        result.append([])
        for x in range(len(listImg)):
            for i in range(multiplier):
                result[y*multiplier].append(listImg[y][x])
        
        for i in range(multiplier-1):
            result.append(result[y*multiplier])

    return pil_base64(Image.fromarray(np.uint8(np.array(result))))

def updateWindow():
    for key in molds.keys():
        window[key].update(image_data=resizeAndConvert(newImages[key], 2))
    window['lookingAt'].update(source=resizeAndConvert(newImages[lookingAt], 20))


def GUI():
    global newImages, palletInUse, lookingAt
    sg.theme('Dark Grey 11')


    layout= [[sg.Column([
            [sg.Image(source=resizeAndConvert(newImages[lookingAt], 20), key='lookingAt')]]), #Focus Item
        sg.VSeparator(), sg.Column(sgHelper(['typeImages']), scrollable=False, vertical_scroll_only=True), sg.VSeparator(), sg.Column(sgHelper(['colors']))], #Item chooser and pallet menu
        [
            [sg.HorizontalSeparator()],
            [sg.Button('Apply', key='test', button_color='#aaaa00'), sg.Button('UNDO', button_color='Blue', key='undo'), sg.Button('REDO', button_color='Blue', key='redo'), sg.Text('Type'), sg.DropDown(values=['Gem', 'Metal'], key='matType', enable_events=True)],
            [sg.Text('Material Name: '), sg.Input(size=(10,80), key='filename'), sg.FolderBrowse(target='dir'), sg.Input(key='dir', visible=False), sg.Button('SAVE', key='save', button_color='#00aa00'), sg.Text(key='warning', visible=False, text_color='Red')]
        ]
        ]


    return layout

#Put the pallet from darkest to lightest (recomended) I use https://www.toptal.com/designers/colourcode/freebuild-color-builder# to get the pallets

def itemCreator():
    global newImages, palletInUse, newImages

    pallet= [[0,0,0,0]] + hex_rgb(palletInUse)
    newImages= {}


    for key in molds.keys():#Go thru every type of item that that material can have
        newTexture = [] #List containing the newly made texture
        for y in range(16):
            newTexture.append([])
            for x in range(16):
                if key != 'Mdirty_dust': #The dirty dust texture has to have its brightness reduced to a 80% so its in a separate if
                    newTexture[y].append(pallet[molds[key][y][x]]) #Add the pallet color that represents the number in the mold
                else:
                    newRGBa = [] #Make a new RGBa with brightness reduced
                    for i in range (3): #Go thru RGB
                        newRGBa.append (int(pallet[molds[key][y][x]][i]*0.8)) #Put the brightness of each R, G, B to a 80%
                    
                    newRGBa.append(pallet[molds[key][y][x]][3])#Append the alpha channel
                    newRGBa= tuple(newRGBa) #Make it a tuple so that its compatible
                    newTexture[y].append(newRGBa) #Add it to the new texture

        newTextureResult = Image.fromarray(np.uint8(np.array(newTexture))) #Convert the list with RGBA values to an np.array and later to an image
        #newTextureResult =  newTextureResult.tobytes()
        newImages[key] = newTextureResult

       #  newTextureResult.save(f'{path}{name}/{name}_{key}.png') #Save the image


itemCreator()
window= sg.Window('Texture Maker', layout=GUI())

while True:
    event, values= window.read()
    if event == sg.WINDOW_CLOSED:
        exit()

    if event == 'test':   
        for i in range(9):
            palletInUse[i]= values[f'color{i}'].lstrip('#')
        unReDo['at'] += 1
        unReDo['history'][unReDo['at']]= palletInUse

        itemCreator()
        updateWindow()
            

    if values['matType'] == 'Gem' and matType == 'metal':
        matType= 'gem'

    elif values['matType'] == 'Metal' and matType == 'gem':
        matType= 'metal'
    
    

    if event in molds.keys():
        lookingAt= event
        window['lookingAt'].update(source=resizeAndConvert(newImages[lookingAt], 20))

    for i in range(9):
        if values[f'color{i}'].lstrip('#') != palletInUse[i]:
            window[f'buttoncolor{i}'].update( button_color=(values[f'color{i}'].replace('None', '#ffffff'), values[f'color{i}'].replace('None', '#ffffff')))

    if event == 'undo' and unReDo['at'] != 0:
        unReDo['at'] -= 1
        palletInUse= unReDo['history'][unReDo['at']]
        itemCreator()
        updateWindow()

    if event == 'redo' and unReDo['at'] < len(unReDo['history'])-1:
        unReDo['at'] += 1
        palletInUse= unReDo['history'][unReDo['at']]
        itemCreator()
        updateWindow()

    if event == 'save':
        if values['dir'] == '':


        

        