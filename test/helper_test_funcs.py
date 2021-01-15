
def check_if_feature_class_instance_has_all_member_variables(feature_class_instance):
    obj = feature_class_instance
    exected_members = ["name", "records", "records_counter"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("_")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members
