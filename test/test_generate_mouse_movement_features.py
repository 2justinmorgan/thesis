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
