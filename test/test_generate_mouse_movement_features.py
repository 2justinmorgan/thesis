import pytest
import generate_mouse_movement_features as gen_features

def test_hello():
	assert gen_features.hello("Mike") == "hello Mike"

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
		('x',[487,912,3419.371],[488,915,3419.62],pytest.approx(4.016064257)),
		('x',[50,75,0.001],[55,76,0.092],pytest.approx(54.94505495)),
		('y',[985,102,40.95],[993,94,41],pytest.approx(160)),
		('y',[0,4,0.00005],[3,2,0.0038],pytest.approx(533.333333333))
	])
def test_axis_velocity(axis, tpointA, tpointB, expect):
	assert gen_features.axis_velocity(axis, tpointA, tpointB) == expect

