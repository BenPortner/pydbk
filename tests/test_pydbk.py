from pathlib import Path
from pydbk import pydbk_cli
import shutil

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
    clean_up()
