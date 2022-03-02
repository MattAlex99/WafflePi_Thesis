#!/bin/bash


echo "Network Configuration"
read -p "Geben sie die IP des remote PC ein:" IP_OF_REMOTE_PC;


ROS_MASTER_URI="http:\/\/${IP_OF_REMOTE_PC}$:11311"
ROS_HOSTNAME="$IP_OF_REMOTE_PC"

echo $ROS_MASTER_URI



sed -i -e "s/^export ROS_MASTER_URI=.*/export ROS_MASTER_URI=${ROS_MASTER_URI}/g" ~/.bashrc
sed -i -e "s/^export ROS_HOSTNAME=.*/export ROS_HOSTNAME=$ROS_HOSTNAME/g" ~/.bashrc

source ~/.bashrc
