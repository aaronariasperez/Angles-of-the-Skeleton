#!/usr/bin/env python

import rospy
from tf2_msgs.msg import TFMessage
from skeleton_angles.msg import AngleMessage
import math
import time

esqueletos = []
cont_vertices = 0
rate = 0

#frecuencia de publicacion


def callback(message):

	global esqueletos
	global cont_vertices
	
	#rospy.loginfo(rospy.get_caller_id() + '\nParte: %s\n' +'Valores: \n%s', message.transforms[0].child_frame_id, message.transforms[0].transform)		
	if cont_vertices<15:

		if message.transforms[0].child_frame_id == 'right_elbow_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(0,aux)

		if message.transforms[0].child_frame_id == 'right_hand_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(1,aux)

		if message.transforms[0].child_frame_id == 'right_shoulder_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(2,aux)

		if message.transforms[0].child_frame_id == 'head_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(3,aux)

		if message.transforms[0].child_frame_id == 'torso_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(4,aux)

		if message.transforms[0].child_frame_id == 'neck_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(5,aux)

		if message.transforms[0].child_frame_id == 'right_hip_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(6,aux)

		if message.transforms[0].child_frame_id == 'right_foot_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(7,aux)

		if message.transforms[0].child_frame_id == 'right_knee_1':
			aux = message.transforms[0].transform.translation
			esqueletos.insert(8,aux)

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

def getAngle(vec1, vec2):
	mod1 = math.sqrt(pow(vec1.x,2) + pow(vec1.y,2) + pow(vec1.z,2))
	mod2 = math.sqrt(pow(vec2.x,2) + pow(vec2.y,2) + pow(vec2.z,2))

	producto = vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z

	angle = math.acos((float(producto)/float(mod1*mod2)))

	return math.degrees(angle)


def get_points():
	global pub
	global rate

	pub = rospy.Publisher('angulos', AngleMessage, queue_size=10)

	rospy.init_node('AnglesCalculator', anonymous=True)

	rate = rospy.Rate(1)

	rospy.Subscriber('tf', TFMessage, callback)

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

def calculate_angles():
	global rate
	global pub

	codo_mano = Vector()
	codo_mano.x = esqueletos[1].x - esqueletos[0].x
	codo_mano.y = esqueletos[1].y - esqueletos[0].y
	codo_mano.z = esqueletos[1].z - esqueletos[0].z

	codo_hombro = Vector()
	codo_hombro.x = esqueletos[2].x - esqueletos[0].x
	codo_hombro.y = esqueletos[2].y - esqueletos[0].y
	codo_hombro.z = esqueletos[2].z - esqueletos[0].z

	cuello_cabeza = Vector()
	cuello_cabeza.x = esqueletos[3].x - esqueletos[5].x
	cuello_cabeza.y = esqueletos[3].y - esqueletos[5].y
	cuello_cabeza.z = esqueletos[3].z - esqueletos[5].z

	cuello_torso = Vector()
	cuello_torso.x = esqueletos[4].x - esqueletos[5].x
	cuello_torso.y = esqueletos[4].y - esqueletos[5].y
	cuello_torso.z = esqueletos[4].z - esqueletos[5].z

	rodilla_cadera = Vector()
	rodilla_cadera.x = esqueletos[6].x - esqueletos[8].x
	rodilla_cadera.y = esqueletos[6].y - esqueletos[8].y
	rodilla_cadera.z = esqueletos[6].z - esqueletos[8].z

	rodilla_pie = Vector()
	rodilla_pie.x = esqueletos[7].x - esqueletos[8].x
	rodilla_pie.y = esqueletos[7].y - esqueletos[8].y
	rodilla_pie.z = esqueletos[7].z - esqueletos[8].z

	#print_punto(codo_mano)
	#print_punto(codo_hombro)

	ang_codo = getAngle(codo_mano, codo_hombro)
	ang_cuello = getAngle(cuello_torso, cuello_cabeza)
	ang_rodilla = getAngle(rodilla_pie, rodilla_cadera)

	#mod1 = math.sqrt(pow(codo_mano.x,2) + pow(codo_mano.y,2) + pow(codo_mano.z,2))
	#mod2 = math.sqrt(pow(codo_hombro.x,2) + pow(codo_hombro.y,2) + pow(codo_hombro.z,2))

	#producto = codo_mano.x*codo_hombro.x + codo_mano.y*codo_hombro.y + codo_mano.z*codo_hombro.z

	#angle = math.acos((float(producto)/float(mod1*mod2)))

	#print '***********************'
	#print ('Angulo: %s' % math.degrees(angle))

	#print '*********************'
	#print 'AnguloCodo: %s' % ang_codo

	print '*********************'
	print 'AnguloCuello: %s' % ang_rodilla

	array = []
	array.append(float(ang_codo))
	array.append(float(ang_cuello))
	array.append(float(ang_rodilla))

	pub.publish(array)
	#rate.sleep()


class Vector:
	
	def __init__(self, a=0, b=0, c=0):
		self.x = a
		self.y = b
		self.z = c

if __name__ == '__main__':
	try:
		get_points()
	except rospy.ROSInterruptException:
		pass
