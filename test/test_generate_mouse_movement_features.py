import pytest
import generate_mouse_movement_features as gen_features

def test_hello():
	assert gen_features.hello("Mike") == "hello Mike"

def test_write_stdout(capsys):
	test_input = "hello stdout test case"	
	gen_features.write_stdout(test_input)
	captured = capsys.readouterr()
	assert captured.out == test_input

@pytest.mark.parametrize(
	"pointA,pointB,expect",
	[
		([23,42],[31,45],pytest.approx(0.35877067027057225)),
		([1020,355],[1003,361],pytest.approx(0.3392926144540447))
	])
def test_theta(pointA, pointB, expect):
	assert gen_features.theta(pointA, pointB) == expect

@pytest.mark.parametrize(
	"axis,tpointA,tpointB,expect",
	[
		('v',[1,2,1],[1,2,1],pytest.approx(-1)),
		('',[13,52,7],[18,44,9],pytest.approx(-1)),
		('x',[0,0,0],[1,0,1],pytest.approx(1)),
		('x',[10,20,5],[15,30,5],pytest.approx(0)),
		('x',[487,912,3419.371],[488,915,3419.62],pytest.approx(4.016064257)),
		('x',[50,75,0.001],[55,76,0.092],pytest.approx(54.94505495)),
		('y',[0,2,0],[1,4,1],pytest.approx(2)),
		('x',[100,200,50],[150,300,50],pytest.approx(0)),
		('y',[985,102,40.95],[993,94,41],pytest.approx(160)),
		('y',[0,4,0.00005],[3,2,0.0038],pytest.approx(533.333333333)),
		('yx',[34,99,54],[23,103,55],pytest.approx(-1)),
		('xy',[10,20,1],[15,32,2],pytest.approx(13)),
		('xy',[31,52,30.35],[15,32,30.35],pytest.approx(0)),
		('xy',[56,341,15290.04],[57,341,15290.29],pytest.approx(4.0)),
		('xy',[1490,888,0.92],[1539,831,1.005],pytest.approx(884.3115516689962))
	])
def test_velocity(axis, tpointA, tpointB, expect):
	assert gen_features.velocity(axis, tpointA, tpointB) == expect

def test_safe_file_read(tmpdir):
	temp_file_name = "temp_test_file.txt"
	temp_file_content = "first line\nof this\nrandom file content\n"
	temp_file = tmpdir.join(temp_file_name)
	temp_file.write(temp_file_content)
	temp_file_path = str(tmpdir)+'/'+temp_file_name

	expect_file_content = '\n'.join(temp_file_content.split('\n')[1:])
	actual_file_content = gen_features.safe_open(temp_file_path).read()
	assert actual_file_content == expect_file_content

@pytest.mark.parametrize(
	"csv_line_str,expect",
	[
		("10,20,Left,Pressed,1452,948",[1452,948,20]),
		("291.082999945,291.082,NoButton,Move,544,594",[544,594,291.082])
	])
def test_get_tpoint(csv_line_str, expect):
	assert gen_features.get_tpoint(csv_line_str) == expect

def test_init_features_obj():
	expect = {}
	for feature in gen_features.FEATURES:
		expect[feature] = gen_features.METRICS
	actual = gen_features.init_features_obj()
	assert actual == expect

@pytest.mark.parametrize(
	"feature_name,tpoints,expect",
	[
		(
			"velocity",
			[[34,55,0.334],[33,52,0.397]],
			pytest.approx(50.19488349473618)
		),
		(
			"xvelocity",
			[[34,55,0.334],[33,52,0.397]],
			pytest.approx(15.873015873)
		),
		(
			"yvelocity",
			[[34,55,0.334],[33,52,0.397]],
			pytest.approx(47.619047619)
		),
		(
			"acceleration",
			[[2,4,1],[1,3,2],[2,3,4],[4,8,8]],
			pytest.approx(0.009703194369924173)
		),
		(
			"acceleration",
			[[2,4,1],[1,3,1],[2,3,1],[4,8,1]],
			pytest.approx(0)
		),
		(
			"jerk",
			[
				[3,6,0.1],[2,4,0.3],[1,3,0.6],[5,4,1],
				[6,7,1.1],[8,5,1.4],[5,4,1.6],[2,2,1.9]],
			pytest.approx(1.2602714455166364)
		),
		(
			"jerk",
			[
				[344,108,0.99371],[345,101,0.99914],[347,93,1.0038],[353,90,1.02388],
				[355,90,1.13884],[355,94,1.177483],[357,95,1.201],[358,98,1.237114]],
			pytest.approx(131170.79429774)
		),
		(
			"jerk",
			[
				[3,6,0.1],[2,4,0.1],[1,3,0.1],[5,4,.1],
				[6,7,.1],[8,5,.1],[5,4,.1],[2,2,.1]],
			pytest.approx(0)
		)
	])
def test_get_val(feature_name, tpoints, expect):
	assert gen_features.get_val(feature_name, tpoints) == expect

@pytest.mark.parametrize(
	"offset,nlines,expect_file_content",
	[
		(2,3,["third\n","fourth\n","fifth\n"]),
		(0,2,["first\n","second\n"]),
		(
			1,
			10,
			[
				"second\n",
				"third\n",
				"fourth\n",
				"fifth\n",
				"sixth\n",
				"seventh\n",
				"",
				"",
				"",
				""])
	])
def test_read_nlines(tmpdir, offset, nlines, expect_file_content):
	temp_file_name = "temp_test_file.txt"
	temp_file = tmpdir.join(temp_file_name)
	temp_file_content = "first\nsecond\nthird\nfourth\nfifth\nsixth\nseventh\n"
	temp_file.write(temp_file_content)
	temp_file_path = str(tmpdir)+'/'+temp_file_name
	pytemp_file = open(temp_file_path,'r')

	for i in range(offset):
		pytemp_file.readline()

	actual_file_content = gen_features.read_nlines(pytemp_file, nlines)
	assert actual_file_content == expect_file_content



	

