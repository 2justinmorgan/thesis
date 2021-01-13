import pytest
import helper_test_funcs
import commons as cms
from commons import Session
import importlib


@pytest.fixture(autouse=True)
def before_each():
    import helper_test_funcs
    import commons
    cms = importlib.reload(commons)
    Session = cms.Session


def test_safe_file_read(tmpdir):
    temp_file_name = "temp_test_file.txt"
    temp_file_content = "first line\nof this\nrandom file content\n"
    temp_file = tmpdir.join(temp_file_name)
    temp_file.write(temp_file_content)
    temp_file_path = str(tmpdir) + '/' + temp_file_name

    expect_file_content = '\n'.join(temp_file_content.split('\n')[1:])
    actual_file_content = cms.safe_open(temp_file_path).read()
    assert actual_file_content == expect_file_content


@pytest.mark.parametrize(
    "offset,nlines,expect_file_content",
    [
        (2, 3, ["third\n", "fourth\n", "fifth\n"]),
        (0, 2, ["first\n", "second\n"]),
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
    temp_file_path = str(tmpdir) + '/' + temp_file_name
    pytemp_file = open(temp_file_path, 'r')

    for i in range(offset):
        pytemp_file.readline()

    actual_file_content = cms.read_nlines(pytemp_file, nlines)
    assert actual_file_content == expect_file_content


def test_init_features_obj():
    actual_features_obj = cms.init_features_obj()

    assert len(actual_features_obj) == len(cms.defines.FEATURES)
    for feature in cms.defines.FEATURES:
        helper_test_funcs.check_if_feature_class_instance_has_all_member_variables(actual_features_obj[feature])
        helper_test_funcs.check_if_stats_class_instance_has_all_member_variables(actual_features_obj[feature].stats)
        assert str(type(actual_features_obj[feature])) == "<class 'defines.Feature'>"  # not sure why not isinstance
        assert isinstance(actual_features_obj[feature].stats, cms.defines.Stats)
        assert isinstance(actual_features_obj[feature].stats.range, cms.defines.Range)
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
    "filepath,expect",
    [
        ("../data/raw_mouse_data/test_files/user7/session_0061629194", Session("user7", "session_0061629194")),
        ("training_files/user12/session_5265929106", Session("user12", "session_5265929106")),
    ])
def test_get_session(filepath, expect):
    actual = cms.get_session(filepath)
    assert actual.user == expect.user
    assert actual.id == expect.id


@pytest.mark.parametrize(
    "float_num,to_left_of_decimal,expected_num_digits",
    [
        (35.22142, True, 2),
        (41882.002, True, 5),
        (4.19921, True, 1),
        (0.90024, True, 0),
        (300110128, True, 9),
        (0.0, True, 0),
        (1882, False, 0),
        (99.1234, False, 4),
        (0.0, False, 0),
        (331.992035, False, 6),
        (0.00125, False, 5)
    ]
)
def test_num_digits(float_num, to_left_of_decimal, expected_num_digits):
    assert cms.num_digits(float_num, to_left_of_decimal=to_left_of_decimal) == expected_num_digits


@pytest.mark.parametrize(
    "float_num,expected_num_digits_to_right",
    [
        (0.038, 1),
        (0.35, 0),
        (0.0001003844, 3),
        (0.000000000000, 0),
        (1.0081, 2),
        (200.0, 0),
        (90233.0000018003, 5)
    ]
)
def test_num_zero_decimal_digits(float_num, expected_num_digits_to_right):
    assert cms.num_leading_zero_decimal_digits(float_num) == expected_num_digits_to_right
