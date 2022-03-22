#! /usr/bin/env python





def joints_to_euler(j1,j2,j3,j4):
	roll=0
	pitch=j1
	yaw= j2+j3+j4
	return [roll, pitch, yaw]




print("input j1 then j2 then j3 then j4")
j1=input()
j2=input()
j3=input()
j4=input()


print joints_to_euler(j1,j2,j3,j4)
	

