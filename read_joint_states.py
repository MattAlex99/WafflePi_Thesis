#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import time


class ReadJoints():
    def __init__(self):
        # initiliaze

        rospy.init_node('read', anonymous=False)
        self.cmd_vel = rospy.Subscriber('joint_states', JointState, queue_size=10, callback=callback)
	rospy.loginfo("Node started and repeating")

	rospy.spin()
	
def callback(data):
    rospy.sleep(3)
    rospy.loginfo("I heard %s",data)
    print(arm_group.get_current_pose())

    pass


if __name__ == '__main__':
    try:
        arm_group = moveit_commander.MoveGroupCommander("arm")
	arm_group.set_planner_id("RRTConnectkConfigDefault")
        ReadJoints()
    except:
        rospy.loginfo("reading state node terminated.")

