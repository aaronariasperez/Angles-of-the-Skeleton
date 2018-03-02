#!/usr/bin/env python

import rospy
from Tkinter import *
from tf2_msgs.msg import TFMessage
import math
import time

array_aux = []
esqueletos = []
cont_esqueletos = 0
cont_vertices = 0

def callback(message):

	global esqueletos
	global cont_vertices
	global cont_esqueletos
	global array_aux
	
	#rospy.loginfo(rospy.get_caller_id() + '\nParte: %s\n' +'Valores: \n%s', message.transforms[0].child_frame_id, message.transforms[0].transform)		
	if cont_vertices<15:

		if message.transforms[0].child_frame_id == 'right_elbow_1':
			codo_der = message.transforms[0].transform.translation
			esqueletos.insert(0,codo_der)

		if message.transforms[0].child_frame_id == 'right_hand_1':
			hand_der = message.transforms[0].transform.translation
			esqueletos.insert(1,hand_der)

		if message.transforms[0].child_frame_id == 'right_shoulder_1':
			hombro_der = message.transforms[0].transform.translation
			esqueletos.insert(2,hombro_der)

		cont_vertices+=1
	else:

		cont_vertices=0

		calculate_angles()

		esqueletos = []

		#time.sleep(3)

		
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
    rospy.spin()

def calculate_angles():

	codo_mano = Vector()
	codo_mano.x = esqueletos[1].x - esqueletos[0].x
	codo_mano.y = esqueletos[1].y - esqueletos[0].y
	codo_mano.z = esqueletos[1].z - esqueletos[0].z

	codo_hombro = Vector()
	codo_hombro.x = esqueletos[2].x - esqueletos[0].x
	codo_hombro.y = esqueletos[2].y - esqueletos[0].y
	codo_hombro.z = esqueletos[2].z - esqueletos[0].z

	#print_punto(codo_mano)
	#print_punto(codo_hombro)

	mod1 = math.sqrt(pow(codo_mano.x,2) + pow(codo_mano.y,2) + pow(codo_mano.z,2))
	mod2 = math.sqrt(pow(codo_hombro.x,2) + pow(codo_hombro.y,2) + pow(codo_hombro.z,2))

	producto = codo_mano.x*codo_hombro.x + codo_mano.y*codo_hombro.y + codo_mano.z*codo_hombro.z

	angle = math.acos((float(producto)/float(mod1*mod2)))

	print '***********************'
	print ('Angulo: %s' % math.degrees(angle))


class Vector:
	
	def __init__(self, a=0, b=0, c=0):
		self.x = a
		self.y = b
		self.z = c

if __name__ == '__main__':
	get_points()
	#time.sleep(1)
