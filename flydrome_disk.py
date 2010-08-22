from py2scad import *
import numpy as np
import sys
sys.path.append("/home/floris/src/floris")

# NOTE: I added the disk_w_holes function to a fork of py2scad/highlevel.py, but to make things easy the function is copied below
sys.path.append("/home/floris/src/py2scad_floris/py2scad/py2scad")
from unit_converter import *
import highlevel as h

def disk_w_holes(height, d1, holes=[], hole_mod=''):
    """
    Create a disk with holes in it.
    
    Arguments:
      d1 = diameter of the disk
      height = z dimension of disk
      holes  = list of tuples giving x position, y position and diameter of 
               holes
    """
    
    cyl = Cylinder(h=height,r1=d1*0.5,r2=d1*0.5)
    cylinders = []
    for x,y,r in holes:
        c = Cylinder(h=4*height,r1=0.5*r, r2=0.5*r)
        c = Translate(c,v=[x,y,0],mod=hole_mod)
        cylinders.append(c)
    obj_list = [cyl] + cylinders
    disk = Difference(obj_list)
    return disk
    
# main

# 3-part sandwich disk
disk_thickness = in2m(0.25)
disk_diameter = 1.
disk_insert_diameter = disk_diameter-mm2m(10.)*2.
disk_insert_thickness = mm2m(500)
central_hole_diameter = disk_diameter-0.5

# hole pattern for cameras
hole_diam = in2m(0.265) # 1/4-20 clearance
pat_radius = 0.9/2.
n_holes = 5
hole_ang = 360/float(n_holes)

holes = []
for ang in range(0.,360.,hole_ang):
    x = pat_radius*np.cos(deg2rad(ang))
    y = pat_radius*np.sin(deg2rad(ang))
    holes.append((x,y,hole_diam))
    
# central hole
center_hole = Cylinder(h=1,r1=central_hole_diameter/2., r2=central_hole_diameter/2.)

# assemble the three disks
disk_top = h.disk_w_holes(disk_thickness,disk_diameter,holes,hole_mod='')
disk_top = Difference([disk_top,center_hole])
disk_insert = h.disk_w_holes(disk_insert_thickness,disk_insert_diameter,holes,hole_mod='')
disk_insert = Difference([disk_insert,center_hole])
disk_insert = Translate(disk_insert,v=[0,0,-1*disk_thickness/2.-disk_insert_thickness/2.])
disk_bottom = Translate(disk_top,v=[0,0,-1.5*disk_thickness-disk_insert_thickness])

prog = SCAD_Prog()
prog.add(disk_top)
prog.add(disk_insert)
prog.add(disk_bottom)
prog.fn=60
print prog
prog.write('flydrome_disk.scad')
