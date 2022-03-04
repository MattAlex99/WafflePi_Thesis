#!/bin/bash
# call with: ssh pi@141.28.75.246 'bash -s' < change_turtlebot_ip.sh IP_Host IP_Turtlebot


echo "$1 wird als Host IP genutzt"
ROS_MASTER_URI="http:\/\/$1:11311"


echo "$2 wird als Turtlebot Ip genutzt " 
ROS_HOSTNAME="$2"


sed -i -e "s/^export ROS_MASTER_URI=.*/export ROS_MASTER_URI=${ROS_MASTER_URI}/g" ~/.bashrc
sed -i -e "s/^export ROS_HOSTNAME=.*/export ROS_HOSTNAME=$ROS_HOSTNAME/g" ~/.bashrc

source ~/.bashrc


