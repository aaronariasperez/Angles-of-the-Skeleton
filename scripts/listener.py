#!/usr/bin/env python

from kinect import Kinect
import rospy

#cont=0
kin = Kinect()

def listener(kin):
	#rospy.init_node('listener', anonymous=True)

	# Get values
	#for i in xrange(10):
   	#print cont, kin.get_posture()
   	
   	print kin.get_posture()
   	#cont+=1

    # spin() simply keeps python from exiting until this node is stopped
  	rospy.spin()

if __name__=='__main__':
	# Init the Kinect object
	listener(kin)