
def check_if_range_class_instance_has_all_member_variables(range_class_instance):
    obj = range_class_instance
    exected_members = ["low", "high"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("_")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members


def check_if_stats_class_instance_has_all_member_variables(stats_class_instance):
    obj = stats_class_instance
    exected_members = ["mean", "median", "mode", "stdev", "range"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("_")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members


def check_if_feature_class_instance_has_all_member_variables(feature_class_instance):
    obj = feature_class_instance
    exected_members = ["name", "stats", "records"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("_")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members
