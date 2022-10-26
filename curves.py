import numpy as np

class Curves():
    def getDistance(A,B):
        '''Returns the distance between A[xa,ya,za] and B[xb,yb,zb]'''
        return np.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 ) 

    def getMidpoint(A,B):
        '''Returns the point [xm,ym,zm] between A[xa,ya,za] and B[xb,yb,zb]'''
        return((A+B)/2)
    
    def convertToNpArray(*points):
        '''Returns all the input points, in the form of [x,y,z] , to np.arrays'''
        output = [np.array(el) if not isinstance(el,np.ndarray) else el for el in points ]
        return tuple(output)

    
    def areCoincident(iterator):
        '''Takes a list of points and returns True if any 2 points on the list are coincident, else false'''
        try:
            iterator = iter(iterator)
            first = next(iterator)
            return any(np.array_equal(first, rest) for rest in iterator)
        except StopIteration:
            return True

    def getNormalVector(v):
        '''takes a vector v and returns a generic vector normal to v'''
        if  (v== 0).all():
            raise ValueError('Normal vector cannot be a zero-vector')
        if v[0] == 0:
            n= [1, 0, 0]
        if v[1]== 0:
            n= [0, 1, 0]
        if v[2] == 0:
            n= [0, 0, 1]
        else:
            n= [1, 1, -1.0 * (v[0] + v[1]) / v[2]]
        return np.array(n)
    
    def findCircle3P(A,B,C):        
        '''Returns  the center "C"  and the radius "r" of the circumference passing through  A,B and C '''
        #segments
        CB = Curves.getDistance(C,B)
        CA = Curves.getDistance(C,A)
        AB = Curves.getDistance(A,B)
        #circumradius
        s = (CB + CA + AB) / 2
        r = CB*CA*AB / 4 / np.sqrt(s * (s - CB) * (s - CA) * (s - AB))
        #Circumcenter
        b1 = CB**2 * (CA**2 + AB**2 - CB**2)
        b2 = CA**2 * (CB**2 + AB**2 - CA**2)
        b3 = AB**2 * (CB**2 + CA**2 - AB**2)
        O = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))
        #normalize 
        O /= b1 + b2 + b3
        return(r,O)


    @staticmethod
    def buildArc3P(A,B,C,max_error= 0.3, min_radius=0.2, complementary=False,min_distance=0):
        '''Returns the list of all the points on the arc starting from point A to point C, passing through point B\n
        max_error: used to determinate how may segments are created between the input points:
            error is the difference between a AB line, and   
        min_radius: if the radius of the curve is less than min_radius, A,B,C are returned,default = 0.2\n
        max'''  

        MAX_ERROR_MINIMUM_VALUE = 0.001
        if max_error < MAX_ERROR_MINIMUM_VALUE : max_error = MAX_ERROR_MINIMUM_VALUE
        A,B,C = Curves.convertToNpArray(A,B,C)
        if Curves.areCoincident([A,B,C]):
            raise ValueError('All the 3 points must be different to each other!')
        r,O = Curves.findCircle3P(A,B,C)

        if r <= min_radius: return [A,B,C]
        if complementary: C = O - (C-O)
        output = [A.tolist()]
        iterable = [A,B,C]   
        for i in range(2)   :
            P1 = iterable[i]
            P2 = iterable[i+1]
            distance = Curves.getDistance(P1,P2)
            if distance < min_distance: 
                output.append(P2.tolist())
                return output     
            M = (P1+P2)/2 
            e = r - Curves.getDistance(M,O) 
            steps = 1
            while e >= max_error:
                steps *= 2
                M = (P1+M)/2
                e = r - Curves.getDistance(M,O) 
            Pvector  = P2-P1
            Pversor =Pvector/np.linalg.norm(Pvector) 
            step = distance/steps
            for i in range(1,steps):
                M =P1+ (Pversor * (step * i)) #P is the point on AB
                OMvector = M - O
                OMversor = OMvector / np.linalg.norm(OMvector)
                T =O + OMversor * r #T = target point
                output.append(T.tolist())
        output.append(C.tolist()) 
        return output

   
    @staticmethod
    def buildCircle(C,N,r,sides:int=15):
        '''Returns the list of all the points of the circle of center C, lying on the plane nomral to C->N.'''
        MIN_RADIUS = 0.001
        MIN_SIDES = 3
        if r < MIN_RADIUS : r = MIN_RADIUS
        if not isinstance(sides,int):
            raise ValueError("Sides must be a integer !")
        if sides < MIN_SIDES : sides = MIN_RADIUS
        C,N = Curves.convertToNpArray(C,N)
        if Curves.areCoincident([C,N]):
            raise ValueError('All the 3 points must be different to each other!')

        deg = int(360/sides)
        rad = deg*np.pi/180
        
        n = N-C
        v = Curves.getNormalVector(n)
        vVersor =v/np.linalg.norm(v) 
        nVersor= n/np.linalg.norm(n) 
        vr = vVersor*r
        points=[]
        for step in range(1,sides+1):#int(360/sides)):
            theta = rad*step
            #ROdrigues rotation formula 
            rotatedVector = vr*np.cos(theta) + np.cross(nVersor,vr)*np.sin(theta)+  nVersor*(np.dot(nVersor,vr))*(1-np.cos(theta))
            rotatedVector += C
            points.append(rotatedVector) 
        points.append(points[0])
        return points

    @staticmethod
    def buildPolygon(C,V,N,sides:int=3,radius:float=0):
        ''' Retrurns the vertices of a polygon of number of sides = sides,\n 
        of center C, a vertex V and a point N on the vector normal to the plane '''

        MIN_RADIUS = 0.001
        MIN_SIDES = 3
        if radius < MIN_RADIUS : radius = MIN_RADIUS
        if not isinstance(sides,int): 
            raise ValueError("Sides must be a integer !")

        C,V,N= Curves.convertToNpArray(C,V,N)
        if Curves.areCoincident([C,V,N]):
            raise ValueError('All the 3 points must be different to each other!')
        if sides < MIN_SIDES : sides = MIN_RADIUS
        deg = int(360/sides)
        rad = deg*np.pi/180
        N = N + (C-V)
        n = N-C
        v = V-C
        vVersor =v/np.linalg.norm(v) 
        nVersor= n/np.linalg.norm(n) 
        vr = vVersor*Curves.getDistance(C,V)
        points=[]
        
        for step in range(0,sides):#int(360/sides)):
            theta = rad*step
            #ROdrigues rotation formula 
            rotatedVector = vr*np.cos(theta) + np.cross(nVersor,vr)*np.sin(theta)+  nVersor*(np.dot(nVersor,vr))*(1-np.cos(theta))
            rotatedVector += C
            #points.append(C)
            points.append(rotatedVector) 
        points.append(points[0])
        return points

    @staticmethod
    def buildSlot(C1,C2,N,r:int,resolution:int= 5) :
        #converet to numpy if necessary 
        C1,C2,N = Curves.convertToNpArray(C1,C2,N)
        if Curves.areCoincident([C1,C2,N]):
            raise ValueError('All the 3 points must be different to each other!')
        #n normal 
        n = N-C2
        nVersor = n/np.linalg.norm(n)       
        C1C2 = C1-C2
        C1C2Versor = C1C2/np.linalg.norm(C1C2) 
        p1 = C1C2Versor * r
        p2 = C1C2Versor * -r
        deg = int(90/resolution)
        rad = deg*np.pi/180
        points =[]
        try :
            for step in range(-resolution,resolution+1):
                theta = rad*step
                rotated = p1*np.cos(theta) + np.cross(nVersor,p1)*np.sin(theta)+  nVersor*(np.dot(nVersor,p1))*(1-np.cos(theta))
                rotated += C1
                points.append(rotated)
            for step in range(-resolution,resolution+1):
                theta = rad*step
                rotated = p2*np.cos(theta) + np.cross(nVersor,p2)*np.sin(theta)+  nVersor*(np.dot(nVersor,p2))*(1-np.cos(theta))
                rotated += C2
                points.append(rotated)
            points.append(points[0])
        except TypeError as e:
            print(e)
        return points



# #debug 

# import matplotlib.pyplot as plt
# ax = plt.axes(projection = "3d")

# # A=np.array([2,1,-3])
# # B=np.array([5,2,3])
# # C=np.array([6,8,2])
# #print(Curves.areCoincident([A,B,C])), ,
# A=np.array([603.44, 756.3, 367.85])
# B=np.array([597.04, 756.3, 367.85])
# C=np.array([ 597.04, 756.04, 377.84])
# # # A=np.random.randn(3)
# # # B=np.random.randn(3)
# # # C=np.random.randn(3)

# # x=[]
# # y=[]
# # z=[]
# x2=[]
# y2=[]
# z2=[]
# # k =   np.array(B) - np.array(A)
# # # N =  np.random.randn(3) # take a random vector
# # # N -= N.dot(k) * k / np.linalg.norm(k)**2       # make it orthogonal to k
# # # N /= np.linalg.norm(N)  # normalize it
# # N = Curves.getNormalVector(k)
# # print(np.dot(N,k))
# # N *=  np.random.randint(-3,3)
# # print(N)
# # #N-=A
# # #C=N
# # #N=C
# # #C= C* Curves.getDistance(A,B)
# p =  Curves.buildSlot(A,B,C,r=5.2,resolution=3)
# # #p =  Curves.buildCircle(A,B,5)
# for point in p :
#     x2.append(point[0])
#     y2.append(point[1])
#     z2.append(point[2])
# ax.scatter(A[0],A[1],A[2],c="g")
# ax.scatter(B[0],B[1],B[2],c="r")
# ax.scatter(C[0],C[1],C[2],c="y")
# ax.plot([A[0],B[0]],[A[1],B[1]],[A[2],B[2]])
# ax.plot([B[0],C[0]],[B[1],C[1]],[B[2],C[2]])
# # # C = C+(A-B)
# # # ax.plot([A[0],C[0]],[A[1],C[1]],[A[2],C[2]])
# # #ax.plot([A[0],N[0]],[A[1],N[1]],[A[2],N[2]],c="gray")
# # ax.plot(x,y,z)
# ax.plot(x2,y2,z2, c = "cyan")
# ax.set_box_aspect([ub - lb for lb, ub in (getattr(ax, f'get_{a}lim')() for a in 'xyz')])
# plt.show()