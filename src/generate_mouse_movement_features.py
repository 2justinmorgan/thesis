
import math
import sys
import copy

FEATURES = [
	"velocity",
	"xvelocity",
	"yvelocity",
	"acceleration",
	"jerk",
	"theta"
]

METRICS = {
	"all": [],
	"stdev": 0.0,
	"mean": 0.0,
	"range": []
}

def hello(name):
	return "hello " + str(name)

def write_stdout(content):
	sys.stdout.write(content)

def theta(pointA, pointB):
	deltaX = abs(pointA[0] - pointB[0])
	deltaY = abs(pointA[1] - pointB[1])
	return math.atan2(deltaY, deltaX)

def velocity(axis, tpointA, tpointB):
	deltaAxis = 0
	if axis != 'x' and axis != 'y' and axis != 'xy':
		return -1

	if axis == 'xy':
		xVelocity = velocity('x', tpointA, tpointB)
		yVelocity = velocity('y', tpointA, tpointB)
		return (xVelocity**2 + yVelocity**2)**.5

	if axis == 'x':
		deltaAxis = abs(tpointA[0] - tpointB[0])
	if axis == 'y':
		deltaAxis = abs(tpointA[1] - tpointB[1])

	deltaT = abs(tpointA[2] - tpointB[2])
	return deltaAxis / deltaT if deltaT else 0

def get_val(feature_name, tpoints):
	#
	# need case that returns if feature_name is invalid
	#
	if "velocity" in feature_name:
		if feature_name == "velocity":
			return velocity("xy",tpoints[0],tpoints[1])
		# the first arg, axis, can be 'x' or 'y'
		return velocity(feature_name[0],tpoints[0],tpoints[1])
	
	if feature_name == "acceleration":
		velocityA = velocity('xy',tpoints[0],tpoints[1])
		velocityB = velocity('xy',tpoints[2],tpoints[3])
		deltaT = abs(tpoints[0][2]-tpoints[3][2])
		return abs(velocityA-velocityB) / deltaT if deltaT else 0
	
	if feature_name == "jerk":
		accelerationA = get_val("acceleration",tpoints[:4])
		accelerationB = get_val("acceleration",tpoints[4:])
		deltaT = abs(tpoints[0][2]-tpoints[7][2])
		return abs(accelerationA-accelerationB) / deltaT if deltaT else 0
	
	if feature_name == "theta":
		deltaY = abs(tpoints[0][1]-tpoints[1][1])
		deltaX = abs(tpoints[0][0]-tpoints[1][0])
		return deltaY / deltaX if deltaX else 0

	return -1

def read_nlines(file_obj, n):
	lines_list = [""]*n
	for i in range(n):
		try:
			lines_list[i] = file_obj.readline()
		except Exception as e:
			sys.stderr.write(e)
			return lines_list
	
	return lines_list

def safe_open(file_path):
	try:
		f = open(file_path, 'r')
	except Exception as e:
		sys.stderr.write(str(e))
		sys.exit(1)
	read_nlines(f, 1)
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
	for feature in FEATURES:
		features_obj[feature] = copy.deepcopy(METRICS)
	return features_obj

def record_features(mouse_data_file_path):
	mouse_data_file = safe_open(mouse_data_file_path)
	features_obj = init_features_obj()
	tpoints = [get_tpoint(e) for e in read_nlines(mouse_data_file, 8)]

	for line in mouse_data_file:
		for feature in FEATURES:
			feature_val = get_val(feature, tpoints)
			features_obj[feature]["all"].append(feature_val)
		tpoints.pop()
		tpoints.insert(0, get_tpoint(line))

	return features_obj


