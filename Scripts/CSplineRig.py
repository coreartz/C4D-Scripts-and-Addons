import c4d

def AddOBJXpresso(nodeMaster, obj, name, ny=100, nx=100):
    snode = nodeMaster.CreateNode(nodeMaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, None, x=nx, y=ny)
    snode.SetName(name)
    snode[c4d.GV_OBJECT_OBJECT_ID] = obj
    if name == "Spline":
        outputPort = snode.AddPort(c4d.GV_PORT_OUTPUT,c4d.GV_OBJECT_OPERATOR_OBJECT_OUT)
    else:
        outputPort = snode.AddPort(c4d.GV_PORT_OUTPUT,c4d.ID_BASEOBJECT_GLOBAL_POSITION)

    return snode, outputPort

def AddPointXpresso(nodeMaster, obj, name, ny=100, nx=100):
    node = nodeMaster.CreateNode(nodeMaster.GetRoot(), c4d.ID_OPERATOR_POINT, None, x=nx, y=ny)
    node[c4d.GV_POINT_INPUT_POINT] = name
    inputPort = node.AddPort(c4d.GV_PORT_INPUT, c4d.GV_POINT_INPUT_POSITION)
    return node, inputPort

def main():
    ny = 150
    spline = doc.GetActiveObject()

    if spline is None or not spline.IsInstanceOf(c4d.Ospline):
        c4d.gui.MessageDialog("Select Spline")
        return

    splinecon = c4d.BaseObject(c4d.Onull)
    splinecon.SetName("Spline Controller")
    doc.InsertObject(splinecon)

    xpressotag = c4d.BaseTag(c4d.Texpresso)
    splinecon.InsertTag(xpressotag)
    xpresso = xpressotag.GetNodeMaster()

    splineNode, splineOutputPort = AddOBJXpresso(xpresso, spline, "Spline")

    pcount = spline.GetPointCount()

    for i in range(pcount):
        pposition = spline.GetPoint(i)

        sphere = c4d.BaseObject(c4d.Osphere)
        sphere.SetName("Point {} Controller".format(i))
        sphere.SetAbsPos(pposition)
        sphere[c4d.PRIM_SPHERE_RAD] = 15
        sphere[c4d.ID_BASEOBJECT_XRAY] = True
        sphere[c4d.ID_BASEOBJECT_USECOLOR] = 2
        sphere[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,0,1)

        sphere.InsertUnder(splinecon)

        sphereNode, sphereOutputPort = AddOBJXpresso(xpresso, sphere, "Sphere {}".format(i),ny)
        pointNode, pointInputPort = AddPointXpresso(xpresso, sphere, i ,ny, 250)
        
        splineOutputPort.Connect(pointNode.GetInPort(0))
        sphereOutputPort.Connect(pointNode.GetInPort(2))
        
        ny = ny + 100
        
        
        phong = c4d.BaseTag(c4d.Tphong)
        sphere.InsertTag(phong)

    c4d.EventAdd()

# Execute the script
if __name__ == '__main__':
    main()