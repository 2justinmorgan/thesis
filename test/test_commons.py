import pytest
import commons as cms
import importlib


@pytest.fixture(autouse=True)
def before_each():
    import commons
    cms = importlib.reload(commons)


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
