import numpy as np
import matplotlib.pyplot as plt
from curves import Curves
ax = plt.axes(projection = "3d")
A = [3,-3,4]
B = np.array([10,3,0])
C  = [10,0,10]


x=[]
y=[]
z=[]
for i in range(5):
    # A = [3,-3,4]
    # B = [-3,3,-4]
    # C  = [5,1,2]
    ax = plt.axes(projection = "3d")
    A = np.random.uniform(high=50,size=(1,3))[0]
    B = np.random.uniform(high=50,size=(1,3))[0]
    C = np.random.uniform(high=50,size=(1,3))[0]
    r,O = Curves.findCirce(A,B,C)
    N = np.array([1, 1, -1.0 * (B[0] + B[1]) / B[2]])

    #p = Curves.buildArc3P(A,B,C,max_error=0.2)
    #p = Curves.buildCircle(A,B,r)
    p = Curves.buildSlot(A,B,N,r)
    x=[]
    y=[]
    z=[]
    for point in p :
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter(A[0],A[1],A[2],c="g")
    ax.scatter(B[0],B[1],B[2],c="r")
    ax.scatter(N[0],N[1],N[2],c="y")
    # ax.scatter(O[0],O[1],O[2],c="b")
    ax.plot(x,y,z)
    ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])
    plt.show()
# p = Curves.buildSlot(C1,C2,N,7)