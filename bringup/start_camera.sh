

read -p "should roscore be started y or n (N if it is already running)" START_CORE;

if [ "$START_CORE" = 'y' ]; then
	echo "starting roscore"
	gnome-terminal  -- roscore
else
	echo "not starting roscore"		
fi

gnome-terminal  -- sshpass  ssh pi@141.28.75.246
read -p "Starten sie das Bringup des Roboters und drücken sie y um den bringup fort zu setzen (ssh ppi@141.28.75.246)"

gnome-terminal  -- sshpass  ssh pi@141.28.75.246
read -p "please execute 'roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch' and then press any key to continue"

echo "starting image view"
gnome-terminal  -- rqt_image_view






read -p "press y if you want to reconfigure the cammera" START_RECONFIGURE;

if [ "$START_RECONFIGURE" = 'y' ]; then
	echo "starting roscore"
	gnome-terminal  -- rosrun rqt_reconfigure rqt_reconfigure
else
	echo "not starting roscore"		
fi

