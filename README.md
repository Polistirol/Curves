# Curves

A python utility to get the coordinates of sets of points belonging to geometrical shapes.

The idea behind this project was the need to have a quick graphical rapresentation of the 3D paths of CNC programs, as only minimun amount of data is visibile in such code and the real trajectoy is calculated internally by the CN.

To keep the amount of output data under control, Curves operates an andjustable segmentation algorithm, to effectively plot or manipulate set of points from minimal input

###### Features
- Arcs segmentation : to split arcs into smaller,straight lines
- Circle segmentation : to build circles made of  a chosen number of straight segments
- Regular shapes : such as polygons and slots
- Geometry helpers: A set of general-pourpose functiuns to help define geometry elements.

**Table of Contents**

- [Curves](#curves)
          - [Features](#features)
- [How to use](#how-to-use)
  - [Example](#example)
- [API](#api)
- [Curves 3D](#curves-3d)
  - [Arc for 3 Points](#arc-for-3-points)
  - [Circle](#circle)
  - [Polygon](#polygon)
  - [Slot](#slot)
- [Geometry Helpers](#geometry-helpers)
  - [Find Circle](#find-circle)
  - [Points  Data](#points--data)
    - [Concident points](#concident-points)

# How to use
Simply clone curves.py from this repository into your project folder and import Curves using:
    from curves import Curves

## Example 
Check example.py for a quick demo of an arc passing for 3 points (uses matplotlib to plot)
    
# API
To better access Curves funtions an API was deployed!

You can find it online at https://curves.deta.dev

Thank you [@Deta Cloud](https://github.com/deta) ! :boom: :heartpulse: 


# Curves 3D
## Arc for 3 Points
<img src="https://curves.deta.dev/resources/A3P.png" alt="drawing" width="250"/>

Returns a list of all the points on the arc starting from point A to point C, passing through point B

	Curves.buildArc3P(A,B,C,max_error, min_radius, complementary,min_distance):

`A, B, C` are the 3 Points the arc is passing by, can be passed as numpy array or a list of number [Xa,Ya,Za]

`max_error` :float  default = 0.3 :  is a value that defines how many segments should the arc be devided into

`min_radius` :float default = 0.2: is the minimim radius, below which the function does not segmentate the curve but returns [A,B,C]

`min_distance` :float default = 0.1: is the minimim distance between A to B or B to C, below which the function does not segmentate the curve but returns the two points

`complementary`: bool default = False : when true returns the points of the complementary arc between A B and C, that  is A -B C 

## Circle

<img src="https://curves.deta.dev/resources/HOLE.png" alt="drawing" width="250"/>
Returns the list of all the points of the circle of center C, lying on the plane nomral to C->N.

	Curves.buildCircle(C,N,r,sides:int=15)

`C` : numpyArray or list [Xc,Yc,Zc] of the center point of the circle.

`N` : numpyArray or list [Xn,Yn,Zn] of the point on the normal to the circle's plane,

`r` :float: radius of the circle

`sides` :int default = number of sides of the circle, higher number will return a smoother circle, minimum value is 3.


## Polygon

<img src="https://curves.deta.dev/resources/POLY.png" alt="drawing" width="250"/>

Retrurns the vertices of a polygon of number of sides = sides, of center C, a vertex V and a point N on the vector normal to the plane.
    Curves.buildPolygon(C,V,N,sides,radius):
`C` : numpyArray or list [Xc,Yc,Zc] of the center point of the polygon.

`V` : numpyArray or list [Xv,Yv,Zv] of the a vertex of the polygon

`N` : numpyArray or list [Xn,Yn,Zn] of a point on the normal vector to the plane, passing by V

`sides` :int default = number of sides of the polygon, minimum value is 3.

## Slot

<img src="https://curves.deta.dev/resources/SLOT.png" alt="drawing" width="250"/>

Retrurns the points of a slot of center C1 and C2 and radius r.

    Curves.buildSlot(C1,C2,N,r,resolution) 

`C1` : numpyArray or list [Xc1,Yc1,Zc1] of the center point of the polygon.

`C2` : numpyArray or list [Xc2,Yc2,Zc2] of the a vertex of the polygon

`N` : numpyArray or list [Xn,Yn,Zn] of a point on the normal to the Slots's plane,passing thru C2

`r` :float : radius of the slot

`resolution` : int default=5 : number of segments of the slot's arcs, higher number will return a smoother arc, minimum value is 3



# Geometry Helpers
## Find Circle
    Curves.findCircle3P(A,B,C)
Returns  the center "C"  and the radius "r" of the circumference passing through  A,B and C

`A, B, C` are the 3 Points on the circle, can be passed as numpy array or a list of number [Xa,Ya,Za]

## Points  Data
### Concident points
    Curves.areCoincident(npaArrayList):

Returns True if any 2 points on the list are coincident, else returns false

`pointList` a iterable containing the points to check
