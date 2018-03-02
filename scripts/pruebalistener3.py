#!/usr/bin/env python

import rospy
from tf2_msgs.msg import TFMessage
from skeleton_angles.msg import AngleMessage
import math
import time

skeleton = []
cont_vertices = 0
rate = 0

#elementos_cuerpo = {'head_1', 'neck_1', 'torso_1', 'left_shoulder_1', 'left_elbow_1', 'left_hand_1', 'right_shoulder_1', 'right_elbow_1', 'right_hand_1', 'left_hip_1', 'left_knee_1', 'left_foot_1', 'right_hip_1', 'right_knee_1', 'right_foot_1'}


def callback(message):

	global skeleton
	global cont_vertices
	
	#rospy.loginfo(rospy.get_caller_id() + '\nParte: %s\n' +'Valores: \n%s', message.transforms[0].child_frame_id, message.transforms[0].transform)		
	if cont_vertices<15:

		fill_skeleton(message)

		cont_vertices+=1
	else:

		cont_vertices=0

		calculate_angles() #this is called only when the skeleton is filled

		skeleton = []

		#time.sleep(3)

def fill_skeleton(message):
	if message.transforms[0].child_frame_id == 'head_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(0,aux)

	if message.transforms[0].child_frame_id == 'neck_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(1,aux)

	if message.transforms[0].child_frame_id == 'torso_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(2,aux)	

	if message.transforms[0].child_frame_id == 'left_shoulder_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(3,aux)

	if message.transforms[0].child_frame_id == 'left_elbow_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(4,aux)

	if message.transforms[0].child_frame_id == 'left_hand_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(5,aux)

	if message.transforms[0].child_frame_id == 'right_shoulder_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(6,aux)

	if message.transforms[0].child_frame_id == 'right_elbow_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(7,aux)

	if message.transforms[0].child_frame_id == 'right_hand_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(8,aux)

	if message.transforms[0].child_frame_id == 'right_hip_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(9,aux)

	if message.transforms[0].child_frame_id == 'right_knee_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(10,aux)

	if message.transforms[0].child_frame_id == 'right_foot_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(11,aux)

	if message.transforms[0].child_frame_id == 'left_hip_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(12,aux)

	if message.transforms[0].child_frame_id == 'left_knee_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(13,aux)

	if message.transforms[0].child_frame_id == 'left_foot_1':
		aux = message.transforms[0].transform.translation
		skeleton.insert(14,aux)
	
		
def print_point(vector):
	print vector.x
	print vector.y
	print vector.z


def getAngle(vec1, vec2):
	mod1 = math.sqrt(pow(vec1.x,2) + pow(vec1.y,2) + pow(vec1.z,2))
	mod2 = math.sqrt(pow(vec2.x,2) + pow(vec2.y,2) + pow(vec2.z,2))

	prod = vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z

	angle = math.acos((float(prod)/float(mod1*mod2)))

	return math.degrees(angle)


def get_points():
	global pub
	global rate

	pub = rospy.Publisher('angles', AngleMessage, queue_size=10)

	rospy.init_node('AnglesCalculator', anonymous=True)

	rate = rospy.Rate(1)

	rospy.Subscriber('tf', TFMessage, callback)

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

def calculate_angles():
	global rate
	global pub

	#for angle 0
	elbow_hand_l = Vector()
	elbow_hand_l.x = skeleton[5].x - skeleton[4].x
	elbow_hand_l.y = skeleton[5].y - skeleton[4].y
	elbow_hand_l.z = skeleton[5].z - skeleton[4].z

	elbow_shoulder_l = Vector()
	elbow_shoulder_l.x = skeleton[3].x - skeleton[4].x
	elbow_shoulder_l.y = skeleton[3].y - skeleton[4].y
	elbow_shoulder_l.z = skeleton[3].z - skeleton[4].z

	#for angle 1
	shoulder_elbow_l = Vector()
	shoulder_elbow_l.x = skeleton[4].x - skeleton[3].x
	shoulder_elbow_l.y = skeleton[4].y - skeleton[3].y
	shoulder_elbow_l.z = skeleton[4].z - skeleton[3].z

	shoulder_neck_l = Vector()
	shoulder_neck_l.x = skeleton[1].x - skeleton[3].x
	shoulder_neck_l.y = skeleton[1].y - skeleton[3].y
	shoulder_neck_l.z = skeleton[1].z - skeleton[3].z

	#for angle 2
	elbow_hand_r = Vector()
	elbow_hand_r.x = skeleton[8].x - skeleton[7].x
	elbow_hand_r.y = skeleton[8].y - skeleton[7].y
	elbow_hand_r.z = skeleton[8].z - skeleton[7].z

	elbow_shoulder_r = Vector()
	elbow_shoulder_r.x = skeleton[6].x - skeleton[7].x
	elbow_shoulder_r.y = skeleton[6].y - skeleton[7].y
	elbow_shoulder_r.z = skeleton[6].z - skeleton[7].z

	#for angle 3
	shoulder_elbow_r = Vector()
	shoulder_elbow_r.x = skeleton[7].x - skeleton[6].x
	shoulder_elbow_r.y = skeleton[7].y - skeleton[6].y
	shoulder_elbow_r.z = skeleton[7].z - skeleton[6].z

	shoulder_neck_r = Vector()
	shoulder_neck_r.x = skeleton[1].x - skeleton[6].x
	shoulder_neck_r.y = skeleton[1].y - skeleton[6].y
	shoulder_neck_r.z = skeleton[1].z - skeleton[6].z

	#for angle 4
	knee_foot_l = Vector()
	knee_foot_l.x = skeleton[11].x - skeleton[10].x
	knee_foot_l.y = skeleton[11].y - skeleton[10].y
	knee_foot_l.z = skeleton[11].z - skeleton[10].z

	knee_hip_l = Vector()
	knee_hip_l.x = skeleton[9].x - skeleton[10].x
	knee_hip_l.y = skeleton[9].y - skeleton[10].y
	knee_hip_l.z = skeleton[9].z - skeleton[10].z

	#for angle 5
	hip_knee_l = Vector()
	hip_knee_l.x = skeleton[10].x - skeleton[9].x
	hip_knee_l.y = skeleton[10].y - skeleton[9].y
	hip_knee_l.z = skeleton[10].z - skeleton[9].z

	hip_torso_l = Vector()
	hip_torso_l.x = skeleton[2].x - skeleton[9].x
	hip_torso_l.y = skeleton[2].y - skeleton[9].y
	hip_torso_l.z = skeleton[2].z - skeleton[9].z

	#for angle 6
	knee_foot_r = Vector()
	knee_foot_r.x = skeleton[14].x - skeleton[13].x
	knee_foot_r.y = skeleton[14].y - skeleton[13].y
	knee_foot_r.z = skeleton[14].z - skeleton[13].z

	knee_hip_r = Vector()
	knee_hip_r.x = skeleton[12].x - skeleton[13].x
	knee_hip_r.y = skeleton[12].y - skeleton[13].y
	knee_hip_r.z = skeleton[12].z - skeleton[13].z

	#for angle 7
	hip_knee_r = Vector()
	hip_knee_r.x = skeleton[13].x - skeleton[12].x
	hip_knee_r.y = skeleton[13].y - skeleton[12].y
	hip_knee_r.z = skeleton[13].z - skeleton[12].z

	hip_torso_r = Vector()
	hip_torso_r.x = skeleton[2].x - skeleton[12].x
	hip_torso_r.y = skeleton[2].y - skeleton[12].y
	hip_torso_r.z = skeleton[2].z - skeleton[12].z

	#print_point(elbow_hand_l)

	#left arm
	ang0 = getAngle(elbow_hand_l, elbow_shoulder_l)
	ang1 = getAngle(shoulder_elbow_l, shoulder_neck_l)

	#right arm
	ang2 = getAngle(elbow_hand_r, elbow_shoulder_r)
	ang3 = getAngle(shoulder_elbow_r, shoulder_neck_r)

	#left leg
	ang4 = getAngle(knee_foot_l, knee_hip_l)
	ang5 = getAngle(hip_knee_l, hip_torso_l)

	#right leg
	ang6 = getAngle(knee_foot_r, knee_hip_r)
	ang7 = getAngle(hip_knee_r, hip_torso_r)


	print '*********************'
	print 'Angulo rodilla: %s' % ang4
	print 'Angulo cadera: %s' % ang5

	array = []
	array.append(float(ang0))
	array.append(float(ang1))

	array.append(float(ang2))
	array.append(float(ang3))

	array.append(float(ang4))
	array.append(float(ang5))

	array.append(float(ang6))
	array.append(float(ang7))

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
