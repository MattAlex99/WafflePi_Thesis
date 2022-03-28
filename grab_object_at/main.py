#! /usr/bin/env python

# Code taken from Robot Ignite Academy. If perfroms multiple movements in the joint task space. The arm
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
import quanternion_from_euler as qfe

print('1 pick up 2 for put down, 3 gymnastics')
operation_mode=input()
names1 = 'position1'
values1 = [0, 0, 0, 0]
target_pose = [0.2, 0, 0.3, 0, 0, 0, 1]

print('please input x')
x = input()
print('please input y')
y = input()
print('please input z')
z = input()
print('please input pitch (in rad)')
pitch = input()
roll = 0
signum_helper = np.sign(float(x) + 0.080001) * np.sign(y)
yaw = np.arctan(np.abs(y) / (np.abs(x) + 0.080001))
if signum_helper != 0:
    yaw = yaw * signum_helper
print(roll, pitch, yaw)
### Calculate final Pose###
qx,qy,qz,qw = qfe.get_quaternion_from_euler(roll,pitch,yaw)
target_pose = [x, y, z, qx, qy, qz, qw]

###Calculate helper psoe###
#This pose has same x any d coords but altering z coords.
qx_h,qy_h,qz_h,qw_h = qfe.get_quaternion_from_euler(0,0,yaw)
helper_pose = [x, y, 0.2, qx_h, qy_h, qz_h, qw_h]


###Mirrored Poses###
#only needed in gymnastics mode
qx_m,qy_m,qz_m,qw_m = qfe.get_quaternion_from_euler(roll,pitch,-yaw)
target_pose_mirrored = [x, -y, z, qx_m, qy_m, qz_m, qw_m]

qx_h_m,qy_h_m,qz_h_m,qw_h_m = qfe.get_quaternion_from_euler(0,0,-yaw)
helper_pose_mirrored = [x, -y, 0.2, qx_h_m, qy_h_m, qz_h_m, qw_h_m]

###### Functions ########

def open_gripper():
    print("Opening Gripper...")
    gripper_group_variable_values[0] = 00.010
    gripper_group.set_joint_value_target(gripper_group_variable_values)
    plan2 = gripper_group.go(wait=True)
    gripper_group.stop()
    gripper_group.clear_pose_targets()
    rospy.sleep(1)


def close_gripper():
    print("Closing Gripper...")
    gripper_group_variable_values[0] = -00.0006
    gripper_group.set_joint_value_target(gripper_group_variable_values)
    plan2 = gripper_group.go(wait=True)
    gripper_group.stop()
    gripper_group.clear_pose_targets()
    rospy.sleep(1)


def set_gripper_by_value(gripper_value):
    print("Moving Gripper...")
    gripper_group_variable_values[0] = gripper_value
    gripper_group.set_joint_value_target(gripper_group_variable_values)
    plan2 = gripper_group.go()
    gripper_group.stop()
    gripper_group.clear_pose_targets()
    rospy.sleep(1)


def move_home():
    arm_group.set_named_target("home")
    print("Executing Move: Home")
    plan1 = arm_group.plan()
    arm_group.execute(plan1, wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()
    variable = arm_group.get_current_pose()
    print(variable.pose)
    #time.sleep(3)
    rospy.sleep(2)


def move_position1():
    arm_group.set_named_target("position1")
    print("Executing Move: Position1")
    plan1 = arm_group.plan()
    arm_group.execute(plan1, wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()
    variable = arm_group.get_current_pose()
    rospy.sleep(1)
    time.sleep(4)
    print(variable.pose)


def take_pose(target_pose):
    # target pose is [x,y,z,qx,qy,qz]
    print("executing move to target_pose")
    print('moving to', target_pose)
    arm_group.set_pose_target(target_pose)
    plan1 = arm_group.plan()
    arm_group.execute(plan1, wait=True)
    arm_group.go(wait=True)
    arm_group.stop()
    arm_group.clear_pose_targets()
    #variable = arm_group.get_current_pose()
    rospy.sleep(2)


###### Setup ########
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_execute_trajectory', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
arm_group = moveit_commander.MoveGroupCommander("arm")
gripper_group = moveit_commander.MoveGroupCommander("gripper")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=1)

# Had probelms with planner failing, Using this planner now. I believe default is OMPL
#arm_group.set_planner_id("RRTConnectkConfigDefault")
arm_group.set_planner_id("RRTkConfigDefault")
#RRTkConfigDefault
# Increased available planning time from 5 to 10 seconds
arm_group.set_planning_time(10);

arm_group.remember_joint_values(names1, values1)

gripper_group_variable_values = gripper_group.get_current_joint_values()

###### Main ########


if operation_mode==1:
    take_pose(helper_pose)
    open_gripper()
    take_pose(target_pose)
    close_gripper()
    take_pose(helper_pose)
    move_home()
elif operation_mode==2:
    take_pose(helper_pose)
    take_pose(target_pose)
    open_gripper()
    take_pose(helper_pose)
    move_home()

elif operation_mode==3:
    ###Pick up and put Down#
    #for i in range (0,3):
        #pick up
        take_pose(helper_pose)
        open_gripper()
        take_pose(target_pose)
        close_gripper()
        take_pose(helper_pose)
        move_home()

        #release mirrored
        take_pose(helper_pose_mirrored)
        take_pose(target_pose_mirrored)
        open_gripper()
        take_pose(helper_pose_mirrored)
        move_home()

        #pick up mirrored
        take_pose(helper_pose_mirrored)
        open_gripper()
        take_pose(target_pose_mirrored)
        close_gripper()
        take_pose(helper_pose_mirrored)
        move_home()

        # release
        take_pose(helper_pose)
        take_pose(target_pose)
        open_gripper()
        take_pose(helper_pose)
        move_home()

moveit_commander.roscpp_shutdown()