from pathlib import Path
from pydbk import pydbk_cli
import shutil
from os.path import getmtime
from datetime import datetime, timedelta

test_dir = Path(__file__).parent.resolve()
source = test_dir / "test.dbk"
destination = test_dir / "temp/"


def clean_up():
    # delete destination folder
    if destination.exists():
        shutil.rmtree(destination)


def test_dry_run():
    clean_up()
    pydbk_cli(["-d", str(source), str(destination)])
    assert not destination.exists()
    clean_up()


def test_extraction():
    clean_up()
    pydbk_cli(["-v", str(source), str(destination)])
    expected_files = [
        Path(destination / "Internal Storage/DCIM/OpenCamera/file0.png"),
        Path(destination / "Internal Storage/file1.txt"),
        Path(destination / "SDcard/file2.txt"),
    ]
    # check all files extracted
    for file in expected_files:
        assert file.exists()
    # check modification dates overwritten
    for file in expected_files:
        time = datetime.fromtimestamp(getmtime(file))
        now = datetime.now()
        assert now - timedelta(minutes=1) <= time <= now + timedelta(seconds=1)
    clean_up()


def test_keep_mod_times():
    clean_up()
    pydbk_cli(["-vt", str(source), str(destination)])
    expected_files = [
        Path(destination / "Internal Storage/DCIM/OpenCamera/file0.png"),
        Path(destination / "Internal Storage/file1.txt"),
        Path(destination / "SDcard/file2.txt"),
    ]
    # check all files extracted
    for file in expected_files:
        assert file.exists()
    # check modification dates kept
    expected_times = [
        datetime.fromisoformat("2023-01-18 00:03:54"),
        datetime.fromisoformat("2023-01-18 00:03:08"),
        datetime.fromisoformat("2023-01-18 00:30:11"),
    ]
    for file, expected in zip(expected_files, expected_times):
        time = datetime.fromtimestamp(getmtime(file))
        assert expected - timedelta(seconds=2) <= time <= expected + timedelta(seconds=2)
    clean_up()
