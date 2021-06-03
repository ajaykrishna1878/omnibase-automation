#!/usr/bin/env python

import rospy
from ros_hackathon.msg import Obstacles

rospy.init_node('obstacle_node')
# initialising the obstacle node

pub = rospy.Publisher('obstacles', Obstacles, queue_size = 2, latched = True)
# publishing function that takes topic name, msg type, queue size and latch as parameters
# we have written a separate msg type called Obstacles which can be found in the msg directory

rate = rospy.Rate(0.5)
# publish at the rate of 0.5 msgs per second

msg = Obstacles()
msg.x_coord = 0
msg.y_coord = 1.5
# initialise the msg type used in the Obstacles.msg msg definition file

while not rospy.is_shutdown():
    msg.y_coord = msg.y_coord + 1.5             # we increment the y coordinate by 1.5 every time
    if msg.y_coord == 6 and msg.x_coord != 6:   # if we reach the end point then restart the loop and publish msgs from the first point again
        msg.x_coord = msg.x_coord + 1.5
        msg.y_coord = 0
    if msg.x_coord == 6 and msg.y_coord == 0:
        msg.x_coord = 0
        msg.y_coord = 1.5
    pub.publish(msg)                            # publish the msg
    rate.sleep()