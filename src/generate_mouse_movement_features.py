
import math
import sys

def hello(name):
	return "hello " + str(name)

def write_stdout(content):
	sys.stdout.write(content)

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
	return deltaAxis / deltaT if deltaT else 0

def velocity(tpointA, tpointB):
	xVelocity = axis_velocity('x', tpointA, tpointB)
	yVelocity = axis_velocity('y', tpointA, tpointB)
	return (xVelocity**2 + yVelocity**2)**.5

def safe_open(file_path):
	try:
		f = open(file_path, 'r')
	except Exception as e:
		sys.stderr.write(str(e))
		sys.exit(1)
	f.readline()
	return f

def get_tpoint(csv_line_str):
	# description: record timestamp,client timestamp,button,state,x,y
	# input (str):
	# 291.082999945,291.082,NoButton,Move,544,594
	# output (list):
	# [544, 594, 291.082]

	csv_line_list = csv_line_str.split(',')
	tpoint_str_list = [csv_line_list[4], csv_line_list[5], csv_line_list[1]]
	tpoint = [float(e) for e in tpoint_str_list]
	return tpoint

def init_features_obj():
	features_obj = {}
	features = [
		"velocity",
		"xvelocity",
		"yvelocity",
		"acceleration",
		"jerk",
		"theta"
	]
	metrics = {
		"all": [],
		"stdev": 0.0,
		"mean": 0.0,
		"range": []
	}
	for feature in features:
		features_obj[feature] = metrics
	return features_obj



