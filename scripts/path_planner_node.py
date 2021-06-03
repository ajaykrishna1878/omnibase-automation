#!/usr/bin/env python

from matplotlib import pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import Point
from matplotlib.patches import Circle
import random
import numpy as np
import math
import sys
import rospy

treex = [0]              # initialising the rrt tree array with start point in origin
treey = [0]

obstacle_array_x = []    # initialising the list of obstacles obtained from the obstacle node
obstacle_array_y = []

#################### Subscribing to the obstacle_node and obtaining coordinates of obstacles#######################
def callback(msg):
    obstacle_array_x.append(msg.x_coord)   # taking the values of the published list of obstacles
    obstacle_array_y.append(msg.y_coord)

rospy.init_node('path_planner_node')                        # initialising subscriber node
sub = rospy.Subscriber('obstacles', Obstacles, callback)    # subscribing to the 'obstacles' topic
rospy.spin()                                                # preventing exit of node until shutdown

############################# Rapidly exploring Random Trees Algorithm ###########################################
count = 0
a = 0
mindist = 1000
maxdist = 1

parx = {}
pary = {}

def distance(x1, y1, x2, y2):
    return math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))

def inside_circle(robLocx, robLocy, obsx, obsy):
	circ = Circle((obsx, obsy), radius = 0.25)
	return circ.contains_point([robLocx, robLocy])

def goalRegion(a1, b1, obsx, obsy):
	circ2 = Circle((obsx, obsy), radius = 0.1)
	return circ2.contains_point([a1, b1])

obstacle_check = 0

for i in range(0, 3000):
	x = round(random.uniform(0, 100), 3)   # randomly generate x coordinate of point
	y = round(random.uniform(0, 100), 3)   # randomly generate y coordinate of point

    	for j in range(0, i):
		dist = distance(treex[j], treey[j], x, y)    # distance between random point and current node
		if mindist >= dist:                          # find a point that is closest to the randomly generated point
		    mindist = dist
		    a = j                                    # note the index of this point
	mindist = 1000                                   # reset the minimum distance back to a very large number

	alpha = treex[a] + ((x - treex[a]) / distance(treex[a], treey[a], x, y))
	beta = treey[a] + ((y - treey[a]) / distance(treex[a], treey[a], x, y))
	# scaling down the randomly generated point such that the maximum distance between each point is 1

	for k in range(0, 14):
		if inside_circle(alpha, beta, obstacle_array_x, obstacle_array_y) == True:  # if point is inside the obstacle circle
			treex.append(treex[i-1])  # add the previous node. Without this, python gives an index error
			treey.append(treey[i-1])
			obstacle_check = 1
		continue

	if obstacle_check == 1:     # if the generated point is in any obstacle, skip following steps
		obstacle_check = 0
		continue

	treex.append(alpha)
	treey.append(beta)

	parx[alpha] = treex[a]
	pary[beta] = treey[a]
	# adding the point to the parent tree array

	if goalRegion(alpha, beta) == True:
		key_listx = list(parx.keys())
		key_listy = list(pary.keys())
		val_listx = list(parx.values())
		val_listy = list(pary.values())     # taking values of the nodes in the parent tree to obtain the path
		rx = alpha
		ry = beta
		colourtreex = []                    # path that will be published
		colourtreey = []


		for cntr in range(0, i-1):  #change: changed count-1 to i-1

			if rx == 50 and ry == 50:
				break
			abcx = val_listx[key_listx.index(rx)]
			rx = abcx
			abcy = val_listy[key_listy.index(ry)]
			ry = abcy

			colourtreex.append(abcx)
			colourtreey.append(abcy)

		'''
		for cntr2 in range(0, cntr-1):
		    plt.plot([colourtreex[cntr2], colourtreex[cntr2+1]], [colourtreey[cntr2], colourtreey[cntr2+1]])

		'''
		# plotting using matplotlib

		'''





		parts of the above plotting loop will also be used for publishing the path




		'''

		break
		# end the loop if goal point is reached
