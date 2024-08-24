import os
import c4d
import random
import math
from c4d import plugins, bitmaps, utils

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1064190

cflick = 0
oldframe = 0
class CFlicker(c4d.plugins.TagData):

    def Init(self, node, isCloneInit=False):

        self.InitAttr(node, float, [c4d.CLIGHT_STRENGTH])
        self.InitAttr(node, int, [c4d.CLIGHT_SEED])
        self.InitAttr(node, float, [c4d.CFLICKER_LIGHT])
        self.InitAttr(node, float, [c4d.CFLICKER_PROB])
        self.InitAttr(node, float, [c4d.CFLICKER_LENGTH])
        self.InitAttr(node, float, [c4d.CFLICKER_LENGTH_VAR])


        #Def Values
        node[c4d.CLIGHT_STRENGTH] = 1
        node[c4d.CLIGHT_SEED] = 189
        node[c4d.CFLICKER_LIGHT] = 0.1
        node[c4d.CFLICKER_PROB] = 0.08
        node[c4d.CFLICKER_LENGTH] = 2
        node[c4d.CFLICKER_LENGTH_VAR] = 2.5

        return True

    def Execute(self, tag, doc, op, bt, priority, flags):
        light = tag.GetObject()
        if not light or light.GetType() != c4d.Olight:
            print("not a Light Source")

        #User values
        lightStrength = tag[c4d.CLIGHT_STRENGTH]
        flickerStrength = tag[c4d.CFLICKER_LIGHT]
        flickerLength = tag[c4d.CFLICKER_LENGTH]
        flickerLengthVar = tag[c4d.CFLICKER_LENGTH_VAR]
        flickerProb = tag[c4d.CFLICKER_PROB]
        seed = tag[c4d.CLIGHT_SEED]

        #Project Frame
        projectTime = doc.GetTime().Get()
        projectFPS = doc.GetFps()
        projectFrame = projectFPS*projectTime

        #RNG
        random.seed(seed + projectFrame)
        flickerProb = 100 - flickerProb * 100
        rng = random.randint(1, 100)
        flickerLengthVar = round(flickerLengthVar)
        flickerLengthVarRNG = random.randint(-(100*flickerLengthVar), 100*flickerLengthVar)

        global cflick
        global oldframe

        #Set Flick Length
        if flickerProb < rng and cflick == 0:
            cflick = round(flickerLength * (1-flickerLengthVarRNG*0.01))
            
        #Fail Safe and Resets
        if 0 > cflick: 
            cflick = 0
        if oldframe > projectFrame:
            cflick = 0    
        if projectFrame == 0:
            cflick = 0
        

        #Set Lightstrength
        if cflick == 0:    
            strength = lightStrength
        elif cflick != 0:
            strength = flickerStrength
        light[c4d.LIGHT_BRIGHTNESS] = strength
            
        #print(str(int(strength*100))+"%")
        
        oldframe = projectFrame
        #Flick Counter
        if cflick != 0:
            cflick = cflick - 1

        return c4d.EXECUTIONRESULT_OK

if __name__ == "__main__":
    #icon
    icon_absolute_path = os.path.join(os.path.dirname(__file__), 'res/icon', 'icon.png')
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    c4d.plugins.RegisterTagPlugin(id=PLUGIN_ID,
                                  str="CFlicker",
                                  info=c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE,
                                  g=CFlicker,
                                  description="OFlickerTag",
                                  icon=plugin_icon)
