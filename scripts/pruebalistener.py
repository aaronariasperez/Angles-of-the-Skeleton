#!/usr/bin/env python

import rospy
from Tkinter import *
from tf2_msgs.msg import TFMessage
import math
import time

cont = 0
array = []
finish = False

def callback(message):
	#for i in range(len(message.transforms)):
	#	rospy.loginfo('\nNum: %s\n', len(message.transforms))
	#	print i
	#	rospy.loginfo(rospy.get_caller_id() + '\nParte: %s\n' +'Valores: \n%s', message.transforms[i].child_frame_id, message.transforms[i].transform)
	global cont
	global array
	global finish

	if cont<15:
		cont += 1
		#rospy.loginfo(rospy.get_caller_id() + '\nParte: %s\n' +'Valores: \n%s', message.transforms[0].child_frame_id, message.transforms[0].transform)		

		if message.transforms[0].child_frame_id == 'right_elbow_1':
			codo_der = message.transforms[0].transform.translation
			array.insert(0,codo_der)

		if message.transforms[0].child_frame_id == 'right_hand_1':
			hand_der = message.transforms[0].transform.translation
			array.insert(1,hand_der)

		if message.transforms[0].child_frame_id == 'right_shoulder_1':
			hombro_der = message.transforms[0].transform.translation
			array.insert(2,hombro_der)
	else:
		finish=True

		
def print_punto(vector):
	print vector.x
	print vector.y
	print vector.z


def get_points():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('pruebesita', anonymous=True)

    rospy.Subscriber('tf', TFMessage, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

def calculate_angles():
	#while not finish:
		#print 'waiting...'
	while not finish:
		dummy=0


	print '***********************'
	print 'codo:'
	print_punto(array[0])
	print '***********************'
	print 'mano:'
	print_punto(array[1])
	print '***********************'
	print 'hombro:'
	print_punto(array[2])

	codo_mano = Vector()
	codo_mano.x = array[1].x - array[0].x
	codo_mano.y = array[1].y - array[0].y
	codo_mano.z = array[1].z - array[0].z

	codo_hombro = Vector()
	codo_hombro.x = array[2].x - array[0].x
	codo_hombro.y = array[2].y - array[0].y
	codo_hombro.z = array[2].z - array[0].z

	#print_punto(codo_mano)
	#print_punto(codo_hombro)

	mod1 = math.sqrt(pow(codo_mano.x,2) + pow(codo_mano.y,2) + pow(codo_mano.z,2))
	mod2 = math.sqrt(pow(codo_hombro.x,2) + pow(codo_hombro.y,2) + pow(codo_hombro.z,2))

	producto = codo_mano.x*codo_hombro.x + codo_mano.y*codo_hombro.y + codo_mano.z*codo_hombro.z

	angle = math.acos((float(producto)/float(mod1*mod2)))

	print '***********************'
	print ('Angulo: %s',math.degrees(angle))


class Vector:
	
	def __init__(self, a=0, b=0, c=0):
		self.x = a
		self.y = b
		self.z = c

if __name__ == '__main__':
	#for i in range(5):
	#	get_points()
	#	calculate_angles()
	#	time.sleep(1)
	#	cont=0
	#	finish = False
	get_points()
	calculate_angles()
