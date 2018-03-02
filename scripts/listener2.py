#!/usr/bin/env python

from kinect import Kinect

# Init the Kinect object
kin = Kinect()

#i=0
#while True:
#	print i, kin.get_posture() 
#	i+=1

# Get values
for i in xrange(30):
    print i, kin.get_posture()