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
plate_thickness = in2m(0.25)
plate_width = 1.5
plate_inner_diameter = 1.
plate_insert_inner_diameter = plate_inner_diameter+mm2m(10.)*2.
plate_insert_thickness = mm2m(500)


# hole pattern for cameras
hole_diam = in2m(0.265) # 1/4-20 clearance
pat_radius = 1.2/2.
n_holes = 5
hole_ang = 360/float(n_holes)

holes = []
for ang in range(0.,360.,hole_ang):
    x = pat_radius*np.cos(deg2rad(ang))
    y = pat_radius*np.sin(deg2rad(ang))
    holes.append((x,y,hole_diam))
    
# central hole
plate_hole = Cylinder(h=1,r1=plate_inner_diameter/2., r2=plate_inner_diameter/2.)
insert_hole = Cylinder(h=1,r1=plate_insert_inner_diameter/2., r2=plate_insert_inner_diameter/2.)

# assemble the three disks
plate_top = plate_w_holes(plate_width,plate_width,plate_thickness,holes,hole_mod='')
plate_top = Difference([plate_top,plate_hole])
plate_insert = plate_w_holes(plate_width,plate_width,plate_insert_thickness,holes,hole_mod='')
plate_insert = Difference([plate_insert,insert_hole])
plate_insert = Translate(plate_insert,v=[0,0,-1*plate_thickness/2.-plate_insert_thickness/2.])
plate_bottom = Translate(plate_top,v=[0,0,-1.5*plate_thickness-plate_insert_thickness])

prog = SCAD_Prog()
prog.add(plate_top)
prog.add(plate_insert)
prog.add(plate_bottom)
prog.fn=60
print prog
prog.write('flydrome_plate.scad')


