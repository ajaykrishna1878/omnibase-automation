#!/usr/bin/env python
import rospy
from ros_hackathon.msg import Obstacles

rospy.init_node('obstacle_node')
pub = rospy.Publisher('obstacles', Obstacles, queue_size = 2, latched = True)
rate = rospy.Rate(0.5)

n1 = 0

n2 = 0

msg = Obstacles()
msg.x_coord = 0
msg.y_coord = 1.5

while not rospy.is_shutdown():
    msg.y_coord = msg.y_coord + 1.5
    if msg.y_coord == 6 and msg.x_coord != 6:
        msg.x_coord = msg.x_coord + 1.5
        msg.y_coord = 0
    if msg.x_coord == 6 and msg.y_coord == 0:
        msg.x_coord = 0
        msg.y_coord = 1.5
    pub.publish(msg)
    rate.sleep()