import pytest
import defines as dfs
import importlib


@pytest.fixture(autouse=True)
def before_each():
    import defines
    dfs = importlib.reload(defines)


def test_locker_point_instance():
    point = dfs.Point(3, 5)
    point.x = 4
    point.y = 6
    with pytest.raises(TypeError) as point_exception_info:
        point.time = 0.170024
    assert " does not allow setting new attributes after object instantiation" in str(point_exception_info.value)


def test_locker_feature_instance():
    feature = dfs.Feature("velocity")
    feature.name = "velocity-2.0"
    with pytest.raises(TypeError) as feature_exception_info:
        feature.some_val = {"apple": "orange"}
    assert " does not allow setting new attributes after object instantiation" in str(feature_exception_info.value)
