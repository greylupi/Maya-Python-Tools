import maya.cmds as cmds
import maya.mel as mel
import math


def create_plane(edge_sel):
    # find world position and width of new plane
    cmds.select(edge_sel)
    obj = cmds.ls(sl=True, o=True)
    obj_name = cmds.listRelatives(obj, parent=True)[0]
    bbox = cmds.exactWorldBoundingBox()
    center_x = (bbox[3]+bbox[0])/2
    center_y = (bbox[4]+bbox[1])/2
    center_z = (bbox[5]+bbox[2])/2
    widths = {bbox[3]-bbox[0], bbox[4]-bbox[1], bbox[5]-bbox[2]}
    plane_width = sorted(widths)[-1]  # sort widths and use the widest

    # find subd values of new plane
    edge_num = len(edge_sel)
    subd_width = math.ceil(edge_num/4.0)
    subd_height = math.ceil((edge_num-(2*subd_width))/2.0)

    # create plane geo
    cmds.select(edge_sel)
    cmds.polyCloseBorder()
    fill_hole = "%s.f[%s]" % (obj_name, cmds.polyEvaluate(obj_name, f=True)-1)
    new_plane = cmds.polyPlane(sx=subd_width,
                                   sy=subd_height,
                                   w=plane_width*0.7,
                                   h=plane_width*0.7,
                                   ch=False)

    # compare inner & outer edgeloops, collapse edge if they don't match
    cmds.select(new_plane)
    new_plane_edge = cmds.ls(sl=True, fl=True)
    if len(new_plane_edge) > len(edge_sel):
        cmds.select(new_plane_edge[-1])
        cmds.polyCollapseEdge()

    # move plane to position, delete hole_fill and history
    cmds.move(center_x, center_y, center_z, new_plane)
    constraint_var = cmds.normalConstraint(fill_hole,
                                            new_plane,
                                            aimVector=(0, 1, 0),
                                            worldUpType=0)
    cmds.delete(new_plane, ch=True)
    cmds.delete(constraint_var)
    cmds.delete(fill_hole)

    return new_plane

#get shape name, from edge selection
shapeName = cmds.ls(sl=True, o=True)
#get polygon/object name from shapeName
obj_name = cmds.listRelatives(shapeName, parent=True)[0]
#select edge loop if not already selected by user
cmds.polySelectSp(loop=True)
#assign selected edge loop to variable  
edge_outer = cmds.ls(sl=True, fl=True)
# create plane... see function 
new_plane = create_plane(edge_outer)
#select new plane
cmds.select(new_plane)
#creates a new poly from our object and new plane created
new_geo_name = cmds.polyUnite(shapeName, new_plane, n=obj_name)[0]
        
cmds.delete(new_geo_name, ch=True)
cmds.isolateSelect(cmds.paneLayout('viewPanes', q=True, pane1=True), addSelected=True)

# select last edge of combined geo, update names for the outer edge
last_edge = (cmds.polyEvaluate(new_geo_name, e=True))-1
last_edge_string = str(new_geo_name)+".e["+str(last_edge)+"]"
new_edge_outer = []
for i in edge_outer:
    new_edge_outer.append(i.replace(obj_name, new_geo_name))

# select inner and outer edge
cmds.select(last_edge_string)
cmds.polySelectSp(loop=True)
edge_inner = cmds.ls(sl=True, fl=True)
mel.eval('polySelectBorderShell 0;')
faces_inner = cmds.ls(sl=True)
cmds.select(edge_inner)
cmds.select(new_edge_outer, add=True)

# run bridge
# average inner verts depending on # of edges in selected edge loop
bridge_node = cmds.polyBridgeEdge(ch=1, divisions=0, bridgeOffset=0)[0]
cmds.select(faces_inner)
avg_num = 7 + int(len(edge_outer)*0.3)
for i in range(avg_num):
    cmds.polyAverageVertex(iterations=10, ch=True)
cmds.setAttr(str(bridge_node) + ".bridgeOffset", k=1)
cmds.select(bridge_node, addFirst=True)
cmds.select(clear=True)