#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState


class ReadJoints():
    def __init__(self):
        # initiliaze
	
        rospy.init_node('read', anonymous=False)
        self.cmd_vel = rospy.Subscriber('joint_states', JointState, queue_size=10, callback=callback)
	rospy.loginfo("Node started and repeating")
	rospy.spin()

def callback(data):
    rospy.loginfo("I heard %s",data)


if __name__ == '__main__':
    try:
        ReadJoints()
    except:
        rospy.loginfo("reading state node terminated.")

