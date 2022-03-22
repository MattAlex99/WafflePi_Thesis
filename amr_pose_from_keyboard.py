#! /usr/bin/env python

#Code taken from Robot Ignite Academy. If perfroms multiple movements in the joint task space. The arm
# will move from the home position to a position above a 40x40mm cube, the pick the cube up, return home,
# then put the cube bacl where it got it from.

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import time
import numpy as np

print('1 for target by joint values, 2 for absolute position')

names1 = 'position1'
values1 = [0,0,0,0]
target_pose=[0.2,0,0.3,0,0,0,1]
input_mode=input()
if input_mode==1:
	print('please input rad of first joint')
	v1=input()
	print('please input rad of second joint')
	v2=input()
	print('please input rad of third joint')
	v3=input()
	print('please input rad of fourth joint')
	v4=input()
	print('determine gripper position')
	print('1 for open')
	print('2 for closed')
	print ('anything else for custom value')
	gripper_position=input()
	names1 = 'position1'
	values1 = [v1,v2,v3,v4]
else:
	print ('please input x')
	x=input()
	print ('please input y')
	y=input()
	print ('please input z')
	z=input()
	print ('please input pitch (in rad)')
	pitch=input()
	roll=0
	
	signum_helper= np.sign(x)* np.sign(y)

	yaw =np.arctan(np.abs(y)/(np.abs(x)+0.08)) 
	print(yaw)
	if signum_helper != 0:
		yaw=yaw*signum_helper


	print (roll,pitch, yaw)

  	qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  	qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  	qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  	qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)


	target_pose=[x,y,z,qx,qy,qz,qw]


###### Functions ########

def open_gripper():
	print ("Opening Gripper...")
	gripper_group_variable_values[0] = 00.010
	gripper_group.set_joint_value_target(gripper_group_variable_values)
	plan2 = gripper_group.go()
	gripper_group.stop()
	gripper_group.clear_pose_targets()
	rospy.sleep(1)

def close_gripper():
	print ("Closing Gripper...")
	gripper_group_variable_values[0] = -00.0006
	gripper_group.set_joint_value_target(gripper_group_variable_values)
	plan2 = gripper_group.go()
	gripper_group.stop()
	gripper_group.clear_pose_targets()
	rospy.sleep(1)
def set_gripper_by_value(gripper_value):
	print ("Moving Gripper...")
	gripper_group_variable_values[0] = gripper_value
	gripper_group.set_joint_value_target(gripper_group_variable_values)
	plan2 = gripper_group.go()
	gripper_group.stop()
	gripper_group.clear_pose_targets()
	rospy.sleep(1)
def move_home():
	arm_group.set_named_target("home")
	print ("Executing Move: Home")
	plan1 = arm_group.plan()
	arm_group.execute(plan1, wait=True)
	arm_group.stop()
	arm_group.clear_pose_targets()
	variable = arm_group.get_current_pose()
	print (variable.pose)
	rospy.sleep(1)


def move_position1():
	arm_group.set_named_target("position1")
	print ("Executing Move: Position1")
	plan1 = arm_group.plan()
	arm_group.execute(plan1, wait=True)
	arm_group.stop()
	arm_group.clear_pose_targets()
	variable = arm_group.get_current_pose()
	rospy.sleep(1)
	time.sleep(2)
	print (variable.pose)

def take_pose(target_pose):
	#target pose is [x,y,z,qx,qy,qz]
	print("executing move to target_pose")	
	print('moving to', target_pose) 
	arm_group.set_pose_target(target_pose)
	plan1 = arm_group.plan()
	arm_group.execute(plan1, wait=True)
	arm_group.stop()
	arm_group.clear_pose_targets()
	variable = arm_group.get_current_pose()
	rospy.sleep(1)
	

###### Setup ########
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_execute_trajectory', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
arm_group = moveit_commander.MoveGroupCommander("arm")
gripper_group = moveit_commander.MoveGroupCommander("gripper")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

#Had probelms with planner failing, Using this planner now. I believe default is OMPL
arm_group.set_planner_id("RRTConnectkConfigDefault")
#Increased available planning time from 5 to 10 seconds
arm_group.set_planning_time(10);

arm_group.remember_joint_values(names1, values1)

gripper_group_variable_values = gripper_group.get_current_joint_values()


###### Main ########

if input_mode==2:

	take_pose(target_pose)
	time.sleep(3)
	print(arm_group.get_current_pose())

if input_mode==1:

	move_position1()	
	time.sleep(3)
	print(arm_group.get_current_pose())
	if gripper_position==1:
		open_gripper()
	elif gripper_position==2:
		close_gripper()
	else:
		while(True):
			print("please input gripper position")
			gripper_value=input()
			set_gripper_by_value(gripper_value)
moveit_commander.roscpp_shutdown()
