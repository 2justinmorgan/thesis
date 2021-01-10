import pytest
import mock
import statistics
import gen_features as genfeatures
from gen_features import Point
from gen_features import TPoint
from gen_features import Feature
import defines
import importlib


@pytest.fixture(autouse=True)
def before_each():
    import gen_features
    import defines
    genfeatures = importlib.reload(gen_features)
    defines = importlib.reload(defines)
    Point = genfeatures.Point
    TPoint = genfeatures.TPoint
    Feature = genfeatures.Feature


def mock_mouse_data_file(tmpdir):
    temp_mouse_data_file_name = "temp_mouse_data_mouse_data_file.csv"
    temp_mouse_data_file_content = \
        "record timestamp,client timestamp,button,state,x,y\n" \
        "0.232000112534,0.234000000171,NoButton,Move,262,2\n" \
        "0.335999965668,0.342999999877,NoButton,Move,361,97\n" \
        "0.624000072479,0.436999999918,NoButton,Move,451,140\n" \
        "0.816999912262,0.827000000048,NoButton,Move,446,140\n" \
        "0.929000139236,0.93600000022,NoButton,Move,209,125\n" \
        "1.1930000782,1.20099999988,NoButton,Move,223,124\n" \
        "1.30400013924,1.31000000006,NoButton,Move,203,115\n" \
        "1.52500009537,1.4040000001,NoButton,Move,138,91\n" \
        "1.52500009537,1.5290000001,NoButton,Move,134,90\n" \
        "1.65600013733,1.6540000001,NoButton,Move,110,99\n" \
        "1.8029999733,1.79400000023,NoButton,Move,99,110\n" \
        "1.9240000248,1.91900000023,NoButton,Move,99,114\n"
    temp_mouse_data_file = tmpdir.join(temp_mouse_data_file_name)
    temp_mouse_data_file.write(temp_mouse_data_file_content)
    temp_mouse_data_filepath = str(tmpdir) + '/' + temp_mouse_data_file_name

    return temp_mouse_data_filepath


def mock_record_features(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    return features_obj


def check_if_range_class_instance_has_all_member_variables(range_class_instance):
    obj = range_class_instance
    exected_members = ["low", "high"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members


def check_if_stats_class_instance_has_all_member_variables(stats_class_instance):
    obj = stats_class_instance
    exected_members = ["mean", "median", "mode", "stdev", "range"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members


def check_if_feature_class_instance_has_all_member_variables(feature_class_instance):
    obj = feature_class_instance
    exected_members = ["name", "stats", "records"]
    actual_members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    assert len(exected_members) == len(actual_members)
    for expected_member in exected_members:
        assert expected_member in actual_members


def test_hello():
    assert genfeatures.hello("Mike") == "hello Mike"


def test_write_stdout(capsys):
    test_input = "hello stdout test case"
    genfeatures.write_stdout(test_input)
    captured = capsys.readouterr()
    assert captured.out == test_input


@pytest.mark.parametrize(
    "point_a,point_b,expect",
    [
        (Point(23, 42), Point(31, 45), pytest.approx(0.35877067027057225)),
        (Point(1020, 355), Point(1003, 361), pytest.approx(0.3392926144540447))
    ])
def test_theta(point_a, point_b, expect):
    assert genfeatures.theta(point_a, point_b) == expect


@pytest.mark.parametrize(
    "axis,tpoint_a,tpoint_b,expect",
    [
        ('v', TPoint(1, 2, 1), TPoint(1, 2, 1), pytest.approx(-1)),
        ('', TPoint(13, 52, 7), TPoint(18, 44, 9), pytest.approx(-1)),
        ('x', TPoint(0, 0, 0), TPoint(1, 0, 1), pytest.approx(1)),
        ('x', TPoint(10, 20, 5), TPoint(15, 30, 5), pytest.approx(0)),
        ('x', TPoint(487, 912, 3419.371), TPoint(488, 915, 3419.62), pytest.approx(4.016064257)),
        ('x', TPoint(50, 75, 0.001), TPoint(55, 76, 0.092), pytest.approx(54.94505495)),
        ('y', TPoint(0, 2, 0), TPoint(1, 4, 1), pytest.approx(2)),
        ('x', TPoint(100, 200, 50), TPoint(150, 300, 50), pytest.approx(0)),
        ('y', TPoint(985, 102, 40.95), TPoint(993, 94, 41), pytest.approx(160)),
        ('y', TPoint(0, 4, 0.00005), TPoint(3, 2, 0.0038), pytest.approx(533.333333333)),
        ('yx', TPoint(34, 99, 54), TPoint(23, 103, 55), pytest.approx(-1)),
        ('xy', TPoint(10, 20, 1), TPoint(15, 32, 2), pytest.approx(13)),
        ('xy', TPoint(31, 52, 30.35), TPoint(15, 32, 30.35), pytest.approx(0)),
        ('xy', TPoint(56, 341, 15290.04), TPoint(57, 341, 15290.29), pytest.approx(4.0)),
        ('xy', TPoint(1490, 888, 0.92), TPoint(1539, 831, 1.005), pytest.approx(884.3115516689962))
    ])
def test_velocity(axis, tpoint_a, tpoint_b, expect):
    assert genfeatures.velocity(axis, tpoint_a, tpoint_b) == expect


@pytest.mark.parametrize(
    "csv_line_str,expect",
    [
        ("10,20,Left,Pressed,1452,948", TPoint(1452, 948, 20)),
        ("291.082999945,291.082,NoButton,Move,544,594", TPoint(544, 594, 291.082))
    ])
def test_get_tpoint(csv_line_str, expect):
    actual = genfeatures.get_tpoint(csv_line_str)
    assert actual.x == expect.x
    assert actual.y == expect.y
    assert actual.time == expect.time


def test_init_features_obj():
    actual_features_obj = genfeatures.init_features_obj()

    assert len(actual_features_obj) == len(defines.FEATURES)
    for feature in genfeatures.FEATURES:
        check_if_feature_class_instance_has_all_member_variables(actual_features_obj[feature])
        check_if_stats_class_instance_has_all_member_variables(actual_features_obj[feature].stats)
        assert str(type(actual_features_obj[feature])) == "<class 'defines.Feature'>"  # not sure why not isinstance
        assert isinstance(actual_features_obj[feature].stats, defines.Stats)
        assert isinstance(actual_features_obj[feature].stats.range, defines.Range)
        assert actual_features_obj[feature].name == feature
        assert actual_features_obj[feature].stats.mean == 0.0
        assert actual_features_obj[feature].stats.median == 0.0
        assert actual_features_obj[feature].stats.mode == 0.0
        assert actual_features_obj[feature].stats.stdev == 0.0
        assert actual_features_obj[feature].stats.range.low == 0.0
        assert actual_features_obj[feature].stats.range.high == 0.0
        assert type(actual_features_obj[feature].records) == list
        assert len(actual_features_obj[feature].records) == 0


@pytest.mark.parametrize(
    "feature_name,tpoints,expect",
    [
        (
            "theta",
            [TPoint(25, 12, 0.33), TPoint(18, 33, 1.4)],
            pytest.approx(1.2490457723982544)),
        (
            "theta",
            [TPoint(556, 273, 8.33927), TPoint(556, 255, 8.4599)],
            pytest.approx(1.5707963267948966)),
        (
            "velocity",
            [TPoint(34, 55, 0.334), TPoint(33, 52, 0.397)],
            pytest.approx(50.19488349473618)),
        (
            "xvelocity",
            [TPoint(34, 55, 0.334), TPoint(33, 52, 0.397)],
            pytest.approx(15.873015873)),
        (
            "yvelocity",
            [TPoint(34, 55, 0.334), TPoint(33, 52, 0.397)],
            pytest.approx(47.619047619)),
        (
            "acceleration",
            [TPoint(2, 4, 1), TPoint(1, 3, 2), TPoint(2, 3, 4), TPoint(4, 8, 8)],
            pytest.approx(0.009703194369924173)),
        (
            "acceleration",
            [TPoint(2, 4, 1), TPoint(1, 3, 1), TPoint(2, 3, 1), TPoint(4, 8, 1)],
            pytest.approx(0)),
        (
            "jerk",
            [
                TPoint(3, 6, 0.1), TPoint(2, 4, 0.3), TPoint(1, 3, 0.6), TPoint(5, 4, 1),
                TPoint(6, 7, 1.1), TPoint(8, 5, 1.4), TPoint(5, 4, 1.6), TPoint(2, 2, 1.9)],
            pytest.approx(1.2602714455166364)),
        (
            "jerk",
            [
                TPoint(344, 108, 0.99371), TPoint(345, 101, 0.99914), TPoint(347, 93, 1.0038), TPoint(353, 90, 1.02388),
                TPoint(355, 90, 1.13884), TPoint(355, 94, 1.177483), TPoint(357, 95, 1.201), TPoint(358, 98, 1.237114)],
            pytest.approx(131170.79429774)),
        (
            "jerk",
            [
                TPoint(3, 6, 0.1), TPoint(2, 4, 0.1), TPoint(1, 3, 0.1), TPoint(5, 4, .1),
                TPoint(6, 7, .1), TPoint(8, 5, .1), TPoint(5, 4, .1), TPoint(2, 2, .1)],
            pytest.approx(0))
    ])
def test_get_val(feature_name, tpoints, expect):
    assert genfeatures.get_val(feature_name, tpoints) == expect


def test_record_features_returned_object_shape(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)

    with mock.patch('gen_features.init_features_obj', wraps=genfeatures.init_features_obj) as init_features_obj_mock:
        actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)
        init_features_obj_mock.assert_called_once()

    assert len(actual_features_obj) == len(defines.FEATURES)
    for feature in genfeatures.FEATURES:
        check_if_feature_class_instance_has_all_member_variables(actual_features_obj[feature])
        check_if_stats_class_instance_has_all_member_variables(actual_features_obj[feature].stats)
        assert str(type(actual_features_obj[feature])) == "<class 'defines.Feature'>"  # not sure why not isinstance
        assert isinstance(actual_features_obj[feature].stats, defines.Stats)
        assert isinstance(actual_features_obj[feature].stats.range, defines.Range)
        assert actual_features_obj[feature].name == feature
        assert actual_features_obj[feature].stats.mean == 0.0
        assert actual_features_obj[feature].stats.median == 0.0
        assert actual_features_obj[feature].stats.mode == 0.0
        assert actual_features_obj[feature].stats.stdev == 0.0
        assert actual_features_obj[feature].stats.range.low == 0.0
        assert actual_features_obj[feature].stats.range.high == 0.0
        assert type(actual_features_obj[feature].records) == list
        assert len(actual_features_obj[feature].records) == 4


def test_record_features_velocity_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["velocity"].records) == 4
    assert actual_features_obj["velocity"].records[0] == pytest.approx(1258.7878152696971)
    assert actual_features_obj["velocity"].records[1] == pytest.approx(1061.1135531890793)
    assert actual_features_obj["velocity"].records[2] == pytest.approx(12.820512816239315)
    assert actual_features_obj["velocity"].records[3] == pytest.approx(2178.662465607613)


def test_record_features_xvelocity_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["xvelocity"].records) == 4
    assert actual_features_obj["xvelocity"].records[0] == pytest.approx(908.256883183739)
    assert actual_features_obj["xvelocity"].records[1] == pytest.approx(957.4468080930284)
    assert actual_features_obj["xvelocity"].records[2] == pytest.approx(12.820512816239315)
    assert actual_features_obj["xvelocity"].records[3] == pytest.approx(2174.3119231744813)


def test_record_features_yvelocity_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["yvelocity"].records) == 4
    assert actual_features_obj["yvelocity"].records[0] == pytest.approx(871.5596353783354)
    assert actual_features_obj["yvelocity"].records[1] == pytest.approx(457.44680831111356)
    assert actual_features_obj["yvelocity"].records[2] == pytest.approx(0.0)
    assert actual_features_obj["yvelocity"].records[3] == pytest.approx(137.61467868192918)


def test_record_features_acceleration_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["acceleration"].records) == 4
    assert actual_features_obj["acceleration"].records[0] == pytest.approx(2101.125299682793)
    assert actual_features_obj["acceleration"].records[1] == pytest.approx(1884.568148013704)
    assert actual_features_obj["acceleration"].records[2] == pytest.approx(52.544863033942164)
    assert actual_features_obj["acceleration"].records[3] == pytest.approx(4094.107861466577)


def test_record_features_jerk_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["jerk"].records) == 4
    assert actual_features_obj["jerk"].records[0] == pytest.approx(546.3725627124735)
    assert actual_features_obj["jerk"].records[1] == pytest.approx(1156.5696055390795)
    assert actual_features_obj["jerk"].records[2] == pytest.approx(1227.7334297968214)
    assert actual_features_obj["jerk"].records[3] == pytest.approx(4026.6489828960184)


def test_record_features_theta_feature(tmpdir):
    temp_mouse_data_filepath = mock_mouse_data_file(tmpdir)
    actual_features_obj = genfeatures.record_features(temp_mouse_data_filepath)

    assert len(actual_features_obj["theta"].records) == 4
    assert actual_features_obj["theta"].records[0] == pytest.approx(0.7647825277718445)
    assert actual_features_obj["theta"].records[1] == pytest.approx(0.4457123126286356)
    assert actual_features_obj["theta"].records[2] == pytest.approx(0.0)
    assert actual_features_obj["theta"].records[3] == pytest.approx(0.06320683189746022)


def test_main_mock_spy():
    genfeatures.commons.check_args = lambda mock_argc, mock_argv: "mouse/data/file/path"
    genfeatures.commons.get_session = lambda mouse_data_file_path: genfeatures.commons.Session()
    genfeatures.record_features = lambda mouse_data_file_path: {"this_is_a_features_obj": True}
    genfeatures.insert_stats = lambda features_obj: None
    genfeatures.formatout.create_json = lambda features_obj, session: None

    with mock.patch('gen_features.record_features', wraps=genfeatures.record_features) as record_features_mock:
        argv = ["this_script_name.py", "data/file/path/user01/session_01"]
        argc = len(argv)
        genfeatures.main(argc, argv)
        record_features_mock.assert_called_once()


def test_insert_stats(tmpdir):
    features_obj = mock_record_features(tmpdir)

    genfeatures.insert_stats(features_obj)

    for feature in features_obj:
        check_if_feature_class_instance_has_all_member_variables(features_obj[feature])
        check_if_stats_class_instance_has_all_member_variables(features_obj[feature].stats)
        stats = features_obj[feature].stats
        assert stats.mean == pytest.approx(statistics.fmean(features_obj[feature].records))
        assert stats.median == pytest.approx(statistics.median(features_obj[feature].records))
        assert stats.mode == pytest.approx(statistics.mode(features_obj[feature].records))
        assert stats.stdev == pytest.approx(statistics.stdev(features_obj[feature].records))
        assert stats.range.low == pytest.approx(min(i for i in features_obj[feature].records if i > 0))
        assert stats.range.high == pytest.approx(max(features_obj[feature].records))
