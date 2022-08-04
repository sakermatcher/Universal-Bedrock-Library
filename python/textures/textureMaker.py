import base64
from variables import molds, icon
import numpy as np #pip install numpy
from PIL import Image
import PySimpleGUI as sg #pip instal pysimplegui
from io import BytesIO
import os

#Global Variables:

palletInUse= ['000000', '0f0f0f', '272727', '4a4a4a', '777777', 'a7a7a7', 'd2d2d2', 'f3f3f3', 'ffffff']#The pallet that is being showed at the moment
newImages={}#The PIL images for every item type... If its for a metal the key starts with an 'M', and for gems the key starts with a 'G', examples: Mchunk, Gchunk
lookingAt= 'Mblock' #The item that the user is looking (the big image at the left), this string refers to a key in the above dictionary
unReDo={'at':0, 'history':{0:['000000', '0f0f0f', '272727', '4a4a4a', '777777', 'a7a7a7', 'd2d2d2', 'f3f3f3', 'ffffff']}} #This helps with the undo and redo buttons; 'history' is a dictionary containing every change to the pallet that youve made, and 'at' just says your point in 'history'

def hex_rgb(values):#Convert a list of hex values to RGBA (Alpha will always be 255)
    final=[]
    for h in values: #Stack Overflow code repurpossed for this proyect
        final.append(list(int(h[i:i+2], 16) for i in (0, 2, 4)))
        final[-1].append(255)

    return final

def pil_base64(image): #Convert PIL images to base64 so that pysimplegui can read them
  img_buffer = BytesIO()
  image.save(img_buffer, format='PNG')
  byte_data = img_buffer.getvalue()
  base64_str = base64.b64encode(byte_data)
  return base64_str #I got this code from stack overflow so I dont know how but it works :)

def resizeAndConvert(img, factor):#Scale a given image (PIL or list) by a factor (2,3,...) and convert it to base64 (using pil_base64)

    listImg= np.array(img).tolist() #Convert the image to a np.array and then to a list that contains RGBA pixel values
    result= [] #The scaled image

    for y in range(len(listImg)): #Go thru every y in the original image
        result.append([]) #Add a empty list (new y level) to result
        for x in range(len(listImg)): #Go thru every x in the original image
            for i in range(factor): #Repeat that RGBA value 'factor' number of times
                result[y*factor].append(listImg[y][x]) #Add that yx RGBA value 'factor' number of times at that x, example: [a,b,c,d,e,f,g,h] -> factor=2 -> [a,a,b,b,c,c,d,d,e,e,f,f,g,g,h,h] were every letter is a different RGBA value
        
        for i in range(factor-1):#Copy the just created line 'factor' number of times -1 because you created the first one before
            result.append(result[y*factor])

    return pil_base64(Image.fromarray(np.uint8(np.array(result)))) #Convert the result list to a np.array and then to a PIL image and later to base64 and return that

def updateWindow(): #Called in the main loop to update the colorchoosers, the button images and the image that you are looking at
    for key in molds.keys():#Go thru every image
        window[key].update(image_data=resizeAndConvert(newImages[key], 2), image_size=(36,36)) #Update that image
    window['lookingAt'].update(source=resizeAndConvert(newImages[lookingAt], 30)) #Update the image youre looking at
    for i in range(9): #Go thru every color
        values[f'color{i}'] = '#'+ palletInUse[i]
        window[f'color{i}'].update('#'+palletInUse[i])
        window[f'buttoncolor{i}'].update( button_color=(values[f'color{i}'], values[f'color{i}'])) #Update the color
            



def GUI():# The layout for the GUI
    global newImages, palletInUse, lookingAt
    sg.theme('Dark Grey 11') #Set the theme


    layout= [[sg.Column([
            [sg.Image(source=resizeAndConvert(newImages[lookingAt], 30), key='lookingAt')]]), #Looking at image
        sg.VSeparator(), sg.Column(sgHelper(['typeImages']), scrollable=False, vertical_scroll_only=True), sg.VSeparator(), sg.Column(sgHelper(['colors']))], #Item chooser and pallet menu
        [
            [sg.HorizontalSeparator()],#Menu below
            [sg.Button('UNDO', button_color='Blue', key='undo'), sg.Button('REDO', button_color='Blue', key='redo')],#Undo and redo button
            [sg.Text('Type:'), sg.DropDown(values=['Gem', 'Metal'], key='matType', enable_events=True)],#Gem/metal chooser
            [sg.Text('Name: '), sg.Input(size=(10,80), key='filename')],#Name chooser
            [sg.FolderBrowse(target='dir', button_text='Save At', button_color='#aaaa00'), sg.Input(key='dir', visible=False), sg.Button('SAVE', key='save', button_color='#00aa00'), sg.Text(key='warning', visible=False, text_color='Red')]#Save at and save buttons
        ]
        ]

    return layout

def sgHelper(helpWith): #Called by GUI helps doing repetitive tasks 
    """
    typeImages, colors
    """
    global unReDo, newImages, palletInUse
    
    if helpWith[0] == 'typeImages': #Make a button for every image type
        x=[[sg.Text('Metal:', justification='center')]] #X is the column for metals
        y=[[sg.Text('Gem:', justification='center')]] #Y is the column for gems
        
        for i in molds.keys(): #Go thru every image type
            if i[0] == 'M': #If the key starts with 'M' its a metal, else its a Gem
                x.append([sg.Button('', key=i, image_size=(36,36), image_data=resizeAndConvert(newImages[i], 2)), sg.Text(i.lstrip('M'))])
            else:
                y.append([sg.Button('', key=i, image_size=(36,36), image_data=resizeAndConvert(newImages[i], 2)), sg.Text(i.lstrip('G'))])

        return [[sg.Column(x, vertical_alignment='top'), sg.VSeparator(), sg.Column(y, vertical_alignment='top')]]

    elif helpWith[0] == 'colors': #Make the colorchooser buttons and the color inputs
        x=[] #The newly made Column
        x.append([sg.Text('Darker (Recomended)')]) #Add the recommended text on top
        for i in range(9): #Make the 9 colors
            x.append([sg.ColorChooserButton('', button_color=('#'+palletInUse[i], '#'+palletInUse[i]), target='color'+str(i), size=(3,1), key=f'buttoncolor{i}'), sg.InputText('#'+palletInUse[i], key=f'color{i}', size=(8,2), text_color='#ffffff', enable_events=True)])
        
        return x+ [[sg.Text('Lighter (Recomended)')]]

#To make the pallets I sometimes use https://www.toptal.com/designers/colourcode/freebuild-color-builder# to get the pallets

def itemCreator(): #Make the images
    global newImages, palletInUse, newImages

    pallet= [[0,0,0,0]] + hex_rgb(palletInUse) #Make the pallet (added a transparent color at the beggining because molds are numbered from 0 to 9 and 0 refers to transparent, and the other numbers refer to a color in the pallet)

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
        newImages[key] = newTextureResult #Add the Image to newImages dict


itemCreator() #Make the images before starting the window so that no errors are found
window= sg.Window('Universal Bedrock Texture-Maker 1.0', layout=GUI(), icon=pil_base64(Image.fromarray(np.uint8(np.array(icon))))) #Initialize the window, the Icon needs to be converted from a list of RGBA values to np array to Pil image and later to base64 so that it can be shown

while True: #Main loop
    event, values= window.read()

    if event == sg.WINDOW_CLOSED: #If window is closed exit the program
        break
    
    if event in molds.keys(): #If the event is an image was clicked
        lookingAt= event #Now youll be looking at that image
        window['lookingAt'].update(source=resizeAndConvert(newImages[lookingAt], 30)) #Update the looking at image

    for i in range(9): #Go thru the 9 colors if check if they have changed
        if values[f'color{i}'].lstrip('#') != palletInUse[i] and event not in ['undo', 'redo'] and len(values[f'color{i}']) == 7: #If it has changed and it wasnt because of a click on undo or redo and the input text is length 7
            try: #Check if its a valid color
                window[f'buttoncolor{i}'].update( button_color=(values[f'color{i}'], values[f'color{i}']))
            except: #Raise a error if it isnt
                window['warning'].update('NOT A VALID COLOR', visible=True, text_color='Red')
            else: #If it is
                for i in range(9):
                    palletInUse[i]= values[f'color{i}'].lstrip('#')#Make a new pallet in use
                unReDo['at'] += 1 #Add 1 to 'at'
                unReDo['history'][unReDo['at']]= palletInUse.copy() #Add the new pallet to history
                itemCreator() #Make the images with the new items
                updateWindow() #Update the window
                window['warning'].update('', visible=False, text_color='Red') #Hide warning text
        elif values[f'color{i}'] == 'None': #If you click the cancel button or close the colorchooser window then the output will be 'None', to handle this I detect if there is a none and just replace it for the color in the pallet that goes there, now you can click on cancel and keep the color
            values[f'color{i}'] = '#'+ palletInUse[i] #Change 'None' for the appropiate color in values
            window[f'color{i}'].update('#'+palletInUse[i]) #Change 'None' for the appropiate color visually


    if event == 'undo' and unReDo['at'] != 0: #Undo Button clicked
        unReDo['at'] -= 1 #Go back in history
        palletInUse= unReDo['history'][unReDo['at']].copy() #Put palletInUse at the place in history youre at
        itemCreator() #Make the newImages
        updateWindow() #Show those images and colors    

    if event == 'redo' and unReDo['at'] < len(unReDo['history'])-1: #Redo Button clicked
        unReDo['at'] += 1 #Go forward in history
        palletInUse= unReDo['history'][unReDo['at']].copy() #Put palletInUse at the place in history youre at
        itemCreator() #Make the newImages
        updateWindow() #Show those images and colors

    if event == 'save': #Save button clicked
        if values['dir'] == '': #If there is no directory selected raise an error
            window['warning'].update('PLIS SELECT A FOLDER TO DOWNLOAD THE TEXTURES', visible=True)
        elif values['matType'] == '': #If no material type was selected raise an error
            window['warning'].update('PLIS SELECT THE MATERIAL TYPE (Gem/Metal)', visible=True)
        elif values['filename'] == '': #If no name was written raise an error
            window['warning'].update('PLIS SELECT A NAME FOR YOUR MATERIAL', visible=True)
        else: #If none of that happen then you can save
            window['warning'].update('SAVED!', visible=True, text_color='#00aa00')
            try: #Create a folder in the directory with the file name, if there is already a folder with that name an error will happen but we can ignore that
                os.mkdir(os.path.join(values['dir'], values['filename'].lower()))
            except:
                pass #If the error is risen do nothing
            finally: 
                for i in newImages.keys(): #Go thru every image
                    if values['matType'][0] == i[0]: #Check if the first letter of matType (>M<etal | >G<em ) matches the first letter of the key (>M<chunk | >G<chunk). In other words check if the Image is the matType selected
                        newImages[i].save(values["dir"].replace("\\", "/") + f'/{values["filename"].lower()}/{values["filename"].lower()}_{i.lstrip("M").lstrip("G")}.png') #Save the PIL image as PNG (replace \ with / because the directory search outputs the directory with backslaches and f strings dont support them). The filename result will be filename_itemtype.png