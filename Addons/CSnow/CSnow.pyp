import os
import c4d
from c4d import plugins, bitmaps


class CSnow (plugins.ObjectData):

    def __init__(self):
        pass

    def Init(self, node):
        #Parameter
        self.InitAttr(node, float, [c4d.SNOW_THICKNESS])
        self.InitAttr(node, float, [c4d.SNOW_VIEWPORT])
        self.InitAttr(node, float, [c4d.SNOW_RENDER])
        self.InitAttr(node, int, [c4d.SNOW_POINTS])
        self.InitAttr(node, float, [c4d.SNOW_POINT_SCALE])
        self.InitAttr(node, float, [c4d.SNOW_ANGLE])
        self.InitAttr(node, int, [c4d.SNOW_SEED])

        #Def Values
        node[c4d.SNOW_THICKNESS] = 8.5
        node[c4d.SNOW_VIEWPORT] = 10
        node[c4d.SNOW_RENDER] = 35
        node[c4d.SNOW_POINTS] = 1500
        node[c4d.SNOW_POINT_SCALE] = 5
        node[c4d.SNOW_ANGLE] = 0.7853981633974497
        node[c4d.SNOW_SEED] = 12345

    def GetVirtualObjects(self, op, hierarchyhelp):
        #OP = Der python generator
        # Alles erstellen
        snow = c4d.BaseObject(c4d.Onull)	#null
        cloner = c4d.BaseObject(1018544)	#MG_Cloner
        sphere = c4d.BaseObject(c4d.Osphere)#sphere
        shader = c4d.BaseList2D(1018561)	#shader effector
        mask = c4d.BaseShader(1026277)		#TerrainMask
        mb = c4d.BaseObject(5125)           #Metaball
        phong = c4d.BaseTag(c4d.Tphong)     #phontag
        con = c4d.BaseObject(1011010)       #connect

        #Kugel settings
        sphere[c4d.PRIM_SPHERE_RAD] = op[c4d.SNOW_POINT_SCALE]	#sphere size

        #Metaball settings
        view_in_val = op[c4d.SNOW_VIEWPORT] - 40        #range mapper viewport
        view_val = view_in_val/(-39)*39
        snowview = view_val+1

        render_in_val = op[c4d.SNOW_RENDER] - 40        #range mapper render
        render_val = render_in_val/(-39)*39
        snowrender = render_val+1

        thick_in_val = op[c4d.SNOW_THICKNESS] - 0.5     #range mapper thickness
        thick_val = thick_in_val/9.5*(-9.5)
        snowthick = thick_val+10

        mb[c4d.METABALLOBJECT_SUBEDITOR] = snowview
        mb[c4d.METABALLOBJECT_SUBRAY] = snowrender
        mb[c4d.METABALLOBJECT_THRESHOLD] = snowthick

        #cloner settings
        cloner[c4d.ID_MG_MOTIONGENERATOR_MODE] = 0                      #Object mode
        cloner[c4d.MG_POLYSURFACE_COUNT] = op[c4d.SNOW_POINTS]          #cloner anzahl
        cloner[c4d.MG_POLYSURFACE_SEED] = op[c4d.SNOW_SEED]             #cloner seed
        cloner[c4d.MG_OBJECT_LINK] = con	                            #Object fürs clonen
        inExcludeData = cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]	#empty "inExcludeData" copy
        inExcludeData.InsertObject(shader, 1)	                        #füge shader in die inExcludeData copy
        cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = inExcludeData	#die copy auf orginal anwenden

        #shader setting
        shader[c4d.ID_MG_BASEEFFECTOR_SCALE_ACTIVE] = False #scale deaktivier
        shader[c4d.ID_MG_BASEEFFECTOR_VISIBILITY] = True	#visibilty aktivieren
        shader.InsertShader(mask)	                        #Fügt shader in eine objekt liste
        shader[c4d.ID_MG_SHADER_SHADER] = mask	            #fügt terrain mask into shader tab
        mask[c4d.XTMASK_SLOPE_MAX] = op[c4d.SNOW_ANGLE]     #Max Slope für terrain maske

        # Childs erstellen
        mb.InsertUnder(snow)
        con.InsertUnder(snow)
        shader.InsertUnder(snow)	#shader ins null
        cloner.InsertUnder(mb)	    #cloner ins null
        sphere.InsertUnder(cloner)	#sphere unter cloner

        for i in range(len(op.GetChildren())):
            master = op.GetChildren()[i]
            copy = master.GetClone()
            copyName = copy.GetName()
            name =  copyName + "_%i"%(i+1)
            copy.SetName(name)
            copy.InsertUnder(con)
            

        mb.InsertTag(phong)      #add phong tag to metaball
        


        return snow	                #return null wo alles drin ist.

if __name__ == "__main__":
    #icon
    icon_absolute_path = os.path.join(os.path.dirname(__file__), 'res/icon', 'icon.png')
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    plugins.RegisterObjectPlugin(
        id = 1057904,
        str = "CSnow",
        g = CSnow,
        description = 'OSnow',
        info = c4d.OBJECT_GENERATOR | c4d.OBJECT_INPUT,
        icon = plugin_icon
    )
