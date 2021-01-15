import pytest
import defines as dfs
import importlib


@pytest.fixture(autouse=True)
def before_each():
    import defines
    dfs = importlib.reload(defines)


def test_feature_class_instance_records_attribute():
    num_of_records = 2500
    first_record = 10.75
    second_record = 0.0
    third_record = 23.005
    feature = dfs.Feature("random-feature", num_of_records=num_of_records)

    assert len(feature.records) == num_of_records
    feature.add_record(first_record)
    feature.add_record(second_record)
    feature.add_record(third_record)
    assert len(feature.records) == num_of_records

    assert feature.records[0] == first_record
    assert feature.records[1] == second_record
    assert feature.records[2] == third_record

    for i in range(3, len(feature.records)):
        assert feature.records[i] == 0.0


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
