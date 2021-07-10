#!/usr/bin/env python

import rospy
#import the Obstacles msg from the msg directory
from omnibase-automation.msg import Obstacles

# initialising the obstacle node
rospy.init_node('obstacle_publisher')

pub = rospy.Publisher('obstacles', Obstacles, queue_size = 2, latched = True)
# publishing function that takes topic name, msg type, queue size and latch as parameters
# we have written a separate msg type called Obstacles which can be found in the msg directory

rate = rospy.Rate(0.5)
# publish at the rate of 0.5 msgs per second

msg = Obstacles()
#starting from first obstacle at (0, 1.5)
msg.x_coord = 0
msg.y_coord = 1.5
# initialise the msg type used in the Obstacles.msg msg definition file

while not rospy.is_shutdown():

    msg.y_coord = msg.y_coord + 1.5
    #incrementing y coordinate every loop
    if msg.y_coord == 6 and msg.x_coord != 6:
        #once y coordinate crosses 4.5, increment x coordinate and reset y coordinate to 0 so as to continue the loop
        msg.x_coord = msg.x_coord + 1.5
        msg.y_coord = 0
    if msg.x_coord == 6 and msg.y_coord == 0:
        #once all nodes are published, loop the publishing process from initial coordinate
        msg.x_coord = 0
        msg.y_coord = 1.5

    #publish the message
    pub.publish(msg)
    rate.sleep()
