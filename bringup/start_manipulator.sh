#!/bin/bash



read -p "should roscore be started y or n (N if it is already running)" START_CORE;

if [ "$START_CORE" = 'y' ]; then
	echo "starting roscore"
	gnome-terminal  -- roscore
else
	echo "not starting roscore"		
fi

gnome-terminal  -- sshpass -p 'Thesis123' ssh pi@141.28.75.246
read -p "Starten sie das Bringup des Roboters und drücken sie y um den bringup fort zu setzen"

echo "starting manipulation"

gnome-terminal  -- roslaunch turtlebot3_manipulation_bringup turtlebot3_manipulation_bringup.launch

echo "starting move group"
gnome-terminal  -- roslaunch turtlebot3_manipulation_moveit_config move_group.launch
echo "starting rviz"
gnome-terminal  -- roslaunch turtlebot3_manipulation_moveit_config moveit_rviz.launch


read -p "should manipulator gui be started y or n" MANIPGUI;

if [ "$MANIPGUI" = "y" ];
	then
	echo "starting manipulation gui"
	sleep 5
	gnome-terminal  -- roslaunch turtlebot3_manipulation_gui turtlebot3_manipulation_gui.launch

	fi




