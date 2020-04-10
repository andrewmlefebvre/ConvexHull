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
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)
	return points

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):

	print("Starting Points: ", points)
	#Sort points by X axis from left to right
	points = sorted(points) 

	#Left most and right most absolutes will always be included
	xmin_point = points[0]
	xmax_point = points[len(points)-1]

	#Set the finished results list to include the left and right also setting it to a "2d" list
	convex_hull_points = [xmin_point, xmax_point]

	#Hulls to divide into
	lefthull = []
	righthull = []

	#For all points not including the leftmost and rightmost
	for i in range(1, len(points) - 1):
		det = triangleArea(xmin_point, xmax_point, points[i])

		#"Upper"
		if det > 0:
			lefthull.append(points[i])
			print("Here")
		#"Lower"
		elif det < 0:
			print("There")
			righthull.append(points[i])
	print("Upper", lefthull)
	print("Lower", righthull)
	merge(lefthull, xmin_point, xmax_point, convex_hull_points)
	merge(righthull, xmax_point, xmin_point, convex_hull_points)

	convex_hull_points = clockwiseSort(convex_hull_points)
	return convex_hull_points


def merge(points, left, right, convex_hull_points): 

	if points:
		extreme_point = 0
		extreme_point_distance = float("-inf")
		candidate_points = []

		for p in points:
			det = triangleArea(left, right, p)
			#print(p, det)
			if det > 0:
				candidate_points.append(p)
				print("Candidate point: ", p)

				if det > extreme_point_distance:
					#print(p, det)
					extreme_point_distance = det
					extreme_point = p

		if extreme_point:
			merge(candidate_points, left, extreme_point, convex_hull_points)
			convex_hull_points.append(extreme_point)
			merge(candidate_points, extreme_point, right, convex_hull_points)