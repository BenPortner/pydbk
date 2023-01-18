from pathlib import Path
from pydbk.pydbk_cli import pydbk_cli
import shutil

source = Path("./test.dbk")
destination = Path("./tmp/")


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
    pydbk_cli([str(source), str(destination)])
    expected_files = [
        Path("./tmp/Internal Storage/DCIM/OpenCamera/file0.png"),
        Path("./tmp/Internal Storage/file1.txt"),
        Path("./tmp/SDcard/file2.txt"),
    ]
    for file in expected_files:
        assert file.exists()
    clean_up()
