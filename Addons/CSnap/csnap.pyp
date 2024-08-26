import os
import c4d
import random
import math
from c4d import plugins, bitmaps, utils

PLUGIN_ID = 1064196

class CSnap(c4d.plugins.TagData):

    def Init(self, node, isCloneInit=False):

        self.InitAttr(node, float, [c4d.CSNAP_HEIGTH])
        node[c4d.CSNAP_HEIGTH] = 0

        return True

    def Execute(self, tag, doc, op, bt, priority, flags):

        def GetLowestPoint(obj):
            deformed_obj = obj.GetDeformCache() if obj.GetDeformCache() else obj.GetCache()
            
            if deformed_obj:
                obj = deformed_obj
            
            if obj.IsInstanceOf(c4d.Opolygon):
                points = obj.GetAllPoints()
                points = [obj.GetMg() * p for p in points]
                minY = min(p.y for p in points)
                return minY
            else:
                points = [c4d.Vector(-1, -1, -1), c4d.Vector(1, -1, -1), c4d.Vector(-1, 1, -1), c4d.Vector(1, 1, -1),
                        c4d.Vector(-1, -1, 1), c4d.Vector(1, -1, 1), c4d.Vector(-1, 1, 1), c4d.Vector(1, 1, 1)]
                points = [c4d.Vector(p.x * obj.GetRad().x, p.y * obj.GetRad().y, p.z * obj.GetRad().z) for p in points]
                points = [obj.GetMg() * p for p in points]
                minY = min(p.y for p in points)
                return minY

        h = tag[c4d.CSNAP_HEIGTH]
            
        obj = tag.GetObject()
        if obj is None:
            return
            
        lowestPointY = GetLowestPoint(obj)
        offset = -lowestPointY + h
        globalPosition = obj.GetMg().off
        globalPosition.y += offset
        newMatrix = obj.GetMg()
        newMatrix.off = globalPosition
        obj.SetMg(newMatrix)

        return c4d.EXECUTIONRESULT_OK

if __name__ == "__main__":
    #icon
    icon_absolute_path = os.path.join(os.path.dirname(__file__), 'res/icon', 'icon.png')
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    c4d.plugins.RegisterTagPlugin(id=PLUGIN_ID,
                                  str="CSnap",
                                  info=c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE,
                                  g=CSnap,
                                  description="OSnapTag",
                                  icon=plugin_icon)
