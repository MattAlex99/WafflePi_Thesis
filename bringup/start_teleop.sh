
read -p "should roscore be started y or n (N if it is already running)" START_CORE;

if [ "$START_CORE" = 'y' ]; then
	echo "starting roscore"
	gnome-terminal  -- roscore
else
	echo "not starting roscore"		
fi

gnome-terminal  -- sshpass -p 'Thesis123' ssh pi@141.28.75.246
read -p "Starten sie das Bringup des Roboters und drücken sie y um den bringup fort zu setzen (ssh ppi@141.28.75.246)"


export TURTLEBOT3_MODEL=${TB3_MODEL}
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

