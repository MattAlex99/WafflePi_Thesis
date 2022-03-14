#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState


class ReadJoints():
    def __init__(self):
        # initiliaze
	
        rospy.init_node('read', anonymous=False)



        # What function to call when you ctrl + c
        rospy.on_shutdown(self.shutdown)

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Subscriber('joint_state', JointState, queue_size=10)

        # TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);
	rospy.loginfo("logind stuff")
        rospy.loginfo (self.cmd_vel.name)
       	rospy.loginfo(self.cmd_vel.position)
        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            # publish the velocity
            print (self.cmd_vel.name)
            print(self.cmd_vel.position)

            # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        ReadJoints()
    except:
        rospy.loginfo("reading state node terminated.")

