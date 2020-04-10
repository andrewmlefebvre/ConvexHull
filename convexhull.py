import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):

	#If both points are on the same Y their yint simply be their Y position
	if(p1[1] == p2[1]):
		return (x, p1[1])

	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given a list of points and a point, returns true if the list contains the point already
'''
def containsPoint(points, pnt):
	if(not points):
		return False
	listLen = len(points)

	for i in range(listLen):
		if(points[i] == pnt):
			return True

	return False
'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c.
Note that this area will be negative
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < -EPSILON;

'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):

	#Do nothing if its empty
	if(not points):
		return points

	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	def angle(p): return (
		(math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key=angle)

'''
Returns true if all points in the list are on the same Y coord
'''
def isVerticalLine(points):
	yVal = points[0][1]
	for i in range(len(points)):
		if yVal != points[i][0]:
			return False
	return True

'''
Given a list of points (x,y)
Sorts the list in increasing
order by x coord.
Note: This function copies its argument and returns a sorted version, leaving the original unchanged.
'''
def sortByXCoord(points):
	sorted_points = points.copy()
	sorted_points.sort(key=lambda x: x[0])
	return sorted_points

'''
Given a list of points (x,y)
Sorts the list in increasing
order by y coord.
Note: This function copies its argument and returns a sorted version, leaving the original unchanged.
'''
def sortByYCoord(points):
	sorted_points = points.copy()
	sorted_points.sort(key=lambda x: x[1])
	return sorted_points

'''
Given two hulls, returns the index of the right most point of the left hull
and the left most point on the right hull
'''
def maxMinXPoints(left, right):
	max_idx = 0
	min_idx = 0
	for i in range(1,len(left)):
		if(left[i][0] > left[max_idx][0]):
			max_idx = i

	for i in range(1,len(right)):
		if(right[i][0] < right[min_idx][0]):
			min_idx = i

	return max_idx, min_idx

'''
Given two hulls, this function finds
the max and min y coords of both sets
'''
def maxMinYPoints(left, right):
	max = left[0][1]
	min = left[0][1]

	for i in range(1, len(left)):
		if(left[i][1] > max):
			max = left[i][1]
		if(left[i][1] < min):
			min = left[i][1]
	for i in range(1, len(right)):
		if(right[i][1] > max):
			max = right[i][1]
		if(right[i][1] < min):
			min = right[i][1]
	return max, min

'''
Given points A, B, and C. Determines whether C is to the left, right
or collinear with the line AB
0 = Collinear
1 = Left
2 = Right
'''
def determineSide(a, b, c):
	side = triangleArea(a, b, c)
	if(side == 0):
		return 0
	if(side < 0):
		return 1
	if(side > 0):
		return 2

'''
Given a list and a point, returns the
index of the point in the list
'''
def find_index(container, point):
	for i in range(0, len(container)):
		if container[i] == point:
			return i

'''
Finds the upper tangent of two convex hulls.

** Invariant **
	- Because this function loops around the edges of the two hulls 
	  and converges on the highest Y intercept, it will run in O(n).  
	  Where n is the len(left) + len(right).

	Loop Invariants:

		Initialization: Upper tangent is initialized to be the closest points of the two hulls.

		Maintenance: Upper tangent is compared to surrounding pairs of points to determine a higher Y-Intercept.

		Termination: The current upper tangent has a higher Y-Intercept than all 
					surrounding pairs and is determined to be the highest.
'''
def upper_tangent(left, right):

	#Gets max and min y values in the two given hulls. Used for yint()
	maxY, minY = maxMinYPoints(left, right)

	# Gets leftmost and rightmost points in the two hulls.
	# Used to find Y-Int X Pos and as starting points for while loop below.
	i,j = maxMinXPoints(left, right)

	# Finds a suitable intercept line by taking the average of points found above.
	X = ((left[i][0] + right[j][0]) / 2)

	left_len = len(left)
	right_len = len(right)

	# Checks if any pair (that is around the current pair) has a higher Y-Intercept
	while (yint(left[i%left_len], right[(j+1)%right_len], X, minY, maxY)[1] > yint(left[i%left_len], right[j%right_len], X, minY, maxY)[1]) \
		or (yint(left[(i-1)%left_len], right[j%right_len], X, minY, maxY)[1] > yint(left[i%left_len], right[j%right_len], X, minY, maxY)[1]) \
		or (yint(left[i % left_len], right[(j-1) % right_len], X, minY, maxY)[1] > yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1])\
		or (yint(left[(i+1) % left_len], right[j % right_len], X, minY, maxY)[1] > yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1]):

		jUpMove = yint(left[i % left_len], right[(j+1) % right_len], X, minY, maxY)[1]
		jDownMove = yint(left[i % left_len], right[(j-1) % right_len], X, minY, maxY)[1]
		iDownMove = yint(left[(i-1) % left_len], right[j % right_len], X, minY, maxY)[1]
		iUpMove = yint(left[(i+1) % left_len], right[(j) % right_len], X, minY, maxY)[1]
		if(jUpMove > iDownMove and jUpMove > iUpMove and jUpMove > jDownMove):
			j = (j + 1) % right_len
		elif(iUpMove >= jUpMove and iUpMove >= jDownMove and iUpMove >= iDownMove):
			i = (i + 1) % left_len
		elif(jDownMove >= jUpMove and jDownMove >= iUpMove and jDownMove >= iDownMove):
			j = (j-1) % right_len
		else:
			i = (i - 1) % left_len

	return left[i%left_len], right[j%right_len]

'''
Finds the lower tangent of two convex hulls.

** Invariant **
	- Because this function loops around the edges of the two hulls 
	  and converges on the lowest Y intercept, it will run in O(n).  
	  Where n is the len(left) + len(right).

	Loop Invariants:

		Initialization: Lower tangent is initialized to be the closest points of the two hulls.

		Maintenance: Lower tangent is compared to surrounding pairs of points to determine a lower Y-Intercept.

		Termination: The current lower tangent has a lower Y-Intercept than all 
					surrounding pairs and is determined to be the lowest
'''
def lower_tangent(left, right):

	#Gets max and min y values in the two given hulls. Used for yint()
	maxY, minY = maxMinYPoints(left, right)

	# Gets leftmost and rightmost points in the two hulls.
	# Used to find Y-Int X Pos and as starting points for while loop below.
	i, j = maxMinXPoints(left, right)

	# Finds a suitable intercept line by taking the average of points found above.
	X = ((left[i][0] + right[j][0]) / 2)

	left_len = len(left)
	right_len = len(right)

	#Checks if any pair (that is around the current pair) has a lower Y-Intercept
	while (yint(left[i % left_len], right[(j+1) % right_len], X, minY, maxY)[1] < yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1]) \
		or (yint(left[(i-1) % left_len], right[j % right_len], X, minY, maxY)[1] < yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1]) \
		or (yint(left[i % left_len], right[(j-1) % right_len], X, minY, maxY)[1] < yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1]) \
		or (yint(left[(i+1) % left_len], right[j % right_len], X, minY, maxY)[1] < yint(left[i % left_len], right[j % right_len], X, minY, maxY)[1]):

		#Checks which pair has the lowest Y-Intercept
		jUpMove = yint(left[i % left_len], right[(j+1) % right_len], X, minY, maxY)[1]
		jDownMove = yint(left[i % left_len], right[(j-1) % right_len], X, minY, maxY)[1]
		iDownMove = yint(left[(i-1) % left_len], right[j % right_len], X, minY, maxY)[1]
		iUpMove = yint(left[(i+1) % left_len], right[(j) % right_len], X, minY, maxY)[1]

		if(jUpMove <= iDownMove and jUpMove <= iUpMove and jUpMove <= jDownMove):
			j = (j + 1) % right_len
		elif(iUpMove < jUpMove and iUpMove < jDownMove and iUpMove < iDownMove):
			i = (i + 1) % left_len
		elif(jDownMove < jUpMove and jDownMove < iUpMove and jDownMove < iDownMove):
			j = (j - 1) % right_len
		else:
			i = (i - 1) % left_len

	return left[i%left_len], right[j%right_len]


'''
A less efficient brute force upper tangent function. This is only used when one or both of the hulls are Vertical Lines.
Using the other upper tangent "upper_tangent()" function will not work on this case.
This function will only be called on small hulls.

**Invariant**

	-All points are checked, and the resultant of this function must be the two points
	 whos intercept on an arbitrary x intercept is the highest combination out of all the
	 points
'''
def brute_upper_tangent(left_point, right_point, left, right):

	# Finds a suitable intercept line by taking the average of the two points found above.
	x_intercept = ((left_point[0] + right_point[0]) / 2)
	maxY, minY = maxMinYPoints(left, right)

	left_len = len(left)
	right_len = len(right)

	highest_intercept = float("-inf")

	for p1 in left:
		for p2 in right:
			icept_x, icept_y = yint(p1, p2, x_intercept, minY, maxY)
			if icept_y > highest_intercept:
				highest_intercept = icept_y
				left_point = p1
				right_point = p2

	return left_point, right_point

'''
A less efficient brute force lower tangent function. This is only used when one or both of the hulls are Vertical Lines.
Using the other lower tangent function "lower_tangent()" will not work on this case.
This function will only be called on small hulls.

**Invariant**

	-All points are checked, and the resultant of this function must be the two points
	 whos intercept on an arbitrary x intercept is the lowest combination out of all the
	 points
'''
def brute_lower_tangent(left_point, right_point, left, right):

	# Finds a suitable intercept line by taking the average of the two points found above.
	x_intercept = ((left_point[0] + right_point[0]) / 2)
	maxY, minY = maxMinYPoints(left, right)

	left_len = len(left)
	right_len = len(right)

	lowest_intercept = float("+inf")

	for p1 in left:
		for p2 in right:
			icept_x, icept_y = yint(p1, p2, x_intercept, minY, maxY)
			if icept_y < lowest_intercept:
				lowest_intercept = icept_y
				left_point = p1
				right_point = p2

	return left_point, right_point



'''
Given a list of points, this function
splits the list into two lists (left and right)
It begins by splitting it directly in half and
then checks if coords with the same x value are separated
between the two halves. If so it will move the similar values to
the left list.

Note: This assumes the list is sorted by x coord in increasing order

Input: [(12, 13), (12, 19), (12, 50), (50, 20)]

Output:
	Left = [(12, 13), (12, 19), (12, 50)]
	Right = [(50, 20)]

** Loop Invariants **

	Initialization: List of points are split into two equal halves +/- 1.

	Maintenance: At iteration i, i values have been shifted from the right list to the left list.
	
	Termination: Lists are split without having points with the same x coord split between the two.
	
'''
def splitList(points):
	offset = 0 #Counts how many points in the right are the same as the last point in the left

	#Initial split
	left = points[:math.ceil((len(points)/2))+offset]
	right = points[math.ceil((len(points)/2))+offset:]
	done = False

	while(not done and len(right) and len(left)):
		#If one point in the right has the same x as the last in the left...pull the one on the right into the left list
		if left[-1][0] == right[0][0]:
			left = points[:math.ceil((len(points)/2))+offset]
			right = points[math.ceil((len(points)/2))+offset:]
			offset+=1
		else:
			done = True

	return left, right

'''
Performs n^3 brute force algorithm on all points to find the hull.
Adds lines that have all points to one side.
Handles collinear points fine.
Returns convex hull in clockwise order.
'''
def naiveAlgorithm(points):
	hull_points = []
	# clockwiseSort(cpy)

	for i in range(len(points)):
		A = points[i]
		onHullA = False
		for j in range(i+1,len(points)):

			B = points[j]
			onHullB = True #Shows whether the point should be on the hull
			numleft=0	#Counts how many points are shown on the left
			numright=0	#Counts how many points are shown on the right

			for k in range(len(points)):

				C = points[k]
				if C == A or C == B:
					continue
				if(determineSide(A,B,C) == 0):
					continue
				elif(determineSide(A,B,C) == 1):
					numleft+=1
				elif(determineSide(A,B,C) == 2):
					numright+=1
				if(numleft and numright):
					onHullB = False
					break
			if(onHullB):
				onHullA = True
				if(not containsPoint(hull_points, B)):
					hull_points.append(B)
		if(not containsPoint(hull_points, A) and onHullA):
			hull_points.append(A)

	clockwiseSort(hull_points)
	return hull_points


'''
Takes two convex hulls and merges them together by connecting them by the upper
and lower tangent. Throws away any points in the middle.
Returns a single convex hull.

**Invariant**

	-The 2 sub-hulls passed to the function must be a valid convex hull.
	-The resultant hull produced by this algorithm must have p points, where
	 as p is equal or less then then number of points within the 2 sub-hulls.
	-All resultant points must comply to the definition of a convex hull.

'''
def mergeHulls(left_side, right_side):

	#Find left most point of right side not assuming order
	left_point = right_side[0]
	for i in range(1, len(right_side)):
		if left_point > right_side[i]:
			left_point = right_side[i]

	#Find right most point of left side not assuming order
	right_point = left_side[0]
	for i in range(1, len(left_side)):
		if right_point < left_side[i]:
			right_point = left_side[i]

	#Check if either side is a single vertical line. If so, brute force to find upper and lower tangent.
	#This is due to a straight lines CW or CCW orientation being undefined
	if(isVerticalLine(left_side) or isVerticalLine(right_side)):
		high_left, high_right = brute_upper_tangent(left_point, right_point, left_side, right_side)
		low_left, low_right = brute_lower_tangent(left_point, right_point, left_side, right_side)
	#If neither are Vertical lines, use normal function
	else:
		high_left, high_right = upper_tangent(left_side, right_side)
		low_left, low_right = lower_tangent(left_side, right_side)

	convex_hull = []
	#Sort in clockwise order
	clockwiseSort(right_side)

	#Find Start and end indicies
	index_end = find_index(right_side, high_right)
	index_start = find_index(right_side, low_right)

	#Add from the right hull to final hull
	convex_hull.append(right_side[index_end])
	while index_start != index_end:
		convex_hull.append(right_side[index_start])
		index_start = (1 + index_start) % len(right_side)

	#Sort in clockwise order
	clockwiseSort(left_side)
	index_end = find_index(left_side, low_left)
	index_start = find_index(left_side, high_left)

	#Add from the left hull to the final hull
	convex_hull.append(left_side[index_end])
	while index_start != index_end:
		convex_hull.append(left_side[index_start])
		index_start = (1 + index_start) % len(left_side)

	return convex_hull

'''
Top level function for compute hull

**Recursive Invariant**

Initilization - Once the points are broken down into lists of 3 or less points they are
               automatically the convex-hull by definition

Maintanence -   All base case sub-hulls are merged together to create a larger, but still
               valid convex-hull.

Termination -   Once all sub-hulls have merged to one the algorithm terminates.
'''
def computeHull(points):

	#Sort by x min -> max
	points = sorted(points)

	# If the line is a vertical line, sort by Y Coord because
	# clockwise sort does not work in this case
	if(isVerticalLine(points)):
		return sortByYCoord(points)

	# Base Case 2 - If there are 3 or less points we show they are on the hull,
	# so we can just return them in clockwise order

	if(len(points) <= 3):
		clockwiseSort(points)
		return points
	# Base Case 3 - Less than 7 points we use n^2 algorithm
	if len(points) <= 6: #Fix for edge (brute)
		return naiveAlgorithm(points)

	#Split points into two sets
	left_side, right_side = splitList(points)

	#Recursivly call computeHull on both sides
	recursive_left = computeHull(left_side)
	recursive_right = computeHull(right_side)

	#Check whether any side is empty. This can be caused by unproportional splits
	if(not recursive_left):
		clockwiseSort(recursive_right)
		return recursive_right
	if(not recursive_right):
		clockwiseSort(recursive_left)
		return recursive_left

	#If either side is less than 4, run naiveAlgorithm rather than real one
	if(len(recursive_left) <= 3 or len(recursive_right) <= 3):
		pnts = recursive_left + recursive_right
		clockwiseSort(pnts)
		final_hull = naiveAlgorithm(pnts)
	else:
		final_hull = mergeHulls(recursive_left, recursive_right)

	clockwiseSort(final_hull)
	return	final_hull
