
import matplotlib.pyplot as plt
from curves import Curves

def prepare_values_for_plt(points):
    x,y,z = [],[],[] 
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2]) 
    return x,y,z       


def pltPlot(A,B,C,points):
    x,y,z = prepare_values_for_plt(points)
    ax = plt.axes(projection = "3d")
    ax.scatter(A[0],A[1],A[2],c="r")
    ax.scatter(B[0],B[1],B[2],c="g")
    ax.scatter(C[0],C[1],C[2],c="y")
    ax.plot(x,y,z,c="cyan")
    ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])
    plt.show()

#### Curves , arc for 3 Points  example
#### Declare 3 points 
A = [3,-3,4]
B = [10,3,0]
C  = [13,0,7]

#### Get all the points on the arc passing thr A, B and C
#### you can have different resolutions by tuning the max error value
points= Curves.buildArc3P(A,B,C,max_error=0.3)

#### Plot the points 
pltPlot(A,B,C,points)


