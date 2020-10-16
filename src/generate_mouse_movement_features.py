
import math

def hello(name):
	return "hello " + str(name)

def theta(pointA, pointB):
	deltaX = abs(pointA[0] - pointB[0])
	deltaY = abs(pointA[1] - pointB[1])
	return math.atan2(deltaY, deltaX)

def axis_velocity(axis, tpointA, tpointB):
	deltaAxis = 0
	if axis != 'x' and axis != 'y':
		return -1

	if axis == 'x':
		deltaAxis = abs(tpointA[0] - tpointB[0])
	if axis == 'y':
		deltaAxis = abs(tpointA[1] - tpointB[1])

	deltaT = abs(tpointA[2] - tpointB[2])
	return deltaAxis / deltaT

