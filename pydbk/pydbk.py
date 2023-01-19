import warnings
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
from typing import List, Dict

source_file = r"C:\Users\Benjamin\Desktop\Handy\Sony Xperia™ Z (C6603)_20160814.dbk"
code_dir = Path(__file__).parent / "extracted"
default_destination = Path("./extracted")


def get_paths(volume: ElementTree.Element) -> List[Dict[str, str]]:
    paths = []
    for path in volume.iter("Paths"):
        for location in path.iter("Location"):
            d = location.attrib
            d["path"] = location.text  # includes volume_path
            paths.append(d)
    return paths


def get_folder_files(
    folder: ElementTree.Element, folder_path: Path
) -> List[Dict[str, str | Path]]:
    files = []
    for file in folder.findall("File"):
        d = file.attrib.copy()
        d["fullpath"] = folder_path / d["Name"]
        files.append(d)
    for subfolder in folder.findall("Folder"):
        subfolder_path = folder_path / subfolder.attrib["Name"]
        files += get_folder_files(subfolder, subfolder_path)
    return files


def scan_volume(volume: ElementTree.Element) -> Dict[str, str | List[Dict]]:
    v = volume.attrib.copy()
    v["paths"] = get_paths(volume)
    volume_path = Path(v["Location"])
    files = []
    for content in volume.findall("Content"):
        for file in content.findall("File"):
            d = file.attrib
            d["fullpath"] = volume_path / d["Name"]
            files.append(d)
        for folder in content.findall("Folder"):
            folder_path = volume_path / folder.attrib["Name"]
            files += get_folder_files(folder, folder_path)
    v["files"] = files
    return v


def scan_volumes(filesystem: ElementTree.Element) -> List[Dict]:
    volumes = []
    for volume in filesystem.findall("Volume"):
        v = scan_volume(volume)
        volumes.append(v)
    return volumes


def join_filelists(filesystem: ElementTree.Element) -> List[Dict]:
    volumes = scan_volumes(filesystem)

    # merge all files from all volumes into one list
    filelist = []
    for volume in volumes:
        filelist += volume["files"]

    return filelist


def check_all_files_present(name_path_map: Dict, content: List[str]) -> None:
    not_in_content = set(name_path_map.keys()) - set(content)
    not_in_filesystem = set(content) - set(name_path_map.keys())
    if len(not_in_content) > 0:
        warnings.warn(
            f"{len(not_in_content)} files were not found under Files/Content."
        )
    if len(not_in_filesystem) > 0:
        warnings.warn(
            f"{len(not_in_filesystem)} files were not found in the file system."
        )
    if len(not_in_content) == len(not_in_filesystem) == 0:
        print(f"Files are complete.")
    return


def get_name_path_map(
    filename: str | Path, check_completeness: bool = True
) -> Dict[str, Path]:

    # read FileSystem.xml and get list of files present in archive
    with ZipFile(filename, "r") as file:
        filesystem = ElementTree.fromstring(file.read("Files/FileSystem.xml"))
        content = [
            Path(f).name for f in file.namelist() if f.startswith("Files/Content/")
        ]

    # get files listed in FileSystem.xml
    filelist = join_filelists(filesystem)

    # add missing ids
    for file in filelist:
        if "Content-Id" not in file:
            file["Content-Id"] = file["Name"]

    # make lookup dict
    name_path_map = {f["Content-Id"]: f["fullpath"] for f in filelist}

    # check if FileSystem.xml is complete
    if check_completeness is True:
        check_all_files_present(name_path_map, content)

    return name_path_map


def extract_files(
    source: str | Path = source_file,
    destination: str | Path = default_destination,
    content_path: str = "Files/Content/",
    check_completeness: bool = True,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:

    name_path_map = get_name_path_map(source, check_completeness=check_completeness)

    with ZipFile(source, "r") as zf:
        for cid, path in name_path_map.items():
            # remove root anchor to make relative path
            path = path.relative_to(path.root)
            if str(path)[0] == "\\":
                path = Path(str(path)[1:])
            clean_path = destination / path
            if not dry_run:
                # make folder
                clean_path.parent.mkdir(parents=True, exist_ok=True)
                # write file
                with open(clean_path, "wb") as f:
                    try:
                        f.write(zf.read(content_path + cid))
                    except KeyError as e:
                        print(e)
            if verbose:
                print(clean_path)
    print(f"Done.")


if __name__ == "__main__":
    extract_files()
