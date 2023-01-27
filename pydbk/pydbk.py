from datetime import datetime
import warnings
import zipfile
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
from typing import List, Dict, Tuple
import os

source_file = r"C:\Users\Benjamin\Desktop\Handy\Sony Xperia™ Z (C6603)_20160814.dbk"
code_dir = Path(__file__).parent / "extracted"
default_destination = Path("./extracted")


class DBKScanner:
    source: Path
    fileindex: ElementTree
    files_in_archive: List[str]
    files_in_fileindex: List[Dict[str, str | Path]]
    content_path: str = "Files/Content/"
    filesystem_path: str = "Files/FileSystem.xml"

    def __init__(self, source: str | Path):

        # filename
        if isinstance(source, str):
            source = Path(source)
        self.source = source

        # read filesystem.xml
        with ZipFile(self.source, "r") as file:
            self.fileindex = ElementTree.fromstring(file.read(self.filesystem_path))

        self.files_in_archive = self._list_files_in_archive()
        self.volumes = self._scan_volumes(self.fileindex)
        self.files_in_fileindex = self._list_files_in_fileindex(fill_content_id=True)

    @staticmethod
    def _get_paths(volume: ElementTree.Element) -> List[Dict[str, str]]:
        """Get all paths in the given volume"""
        paths = []
        for path in volume.iter("Paths"):
            for location in path.iter("Location"):
                d = location.attrib
                d["path"] = location.text  # includes volume_path
                paths.append(d)
        return paths

    def _get_folder_files(
        self, folder: ElementTree.Element, folder_path: Path
    ) -> List[Dict[str, str | Path]]:
        """Get a list of all files in the given folder"""
        files = []
        for file in folder.findall("File"):
            d = file.attrib.copy()
            d["fullpath"] = folder_path / str(d["Name"])
            files.append(d)
        for subfolder in folder.findall("Folder"):
            subfolder_path = folder_path / subfolder.attrib["Name"]
            files += self._get_folder_files(subfolder, subfolder_path)
        return files

    def _scan_volume(self, volume: ElementTree.Element) -> Dict[str, str | List[Dict]]:
        """Get paths and file list for a given volume"""
        v = volume.attrib.copy()
        v["paths"] = self._get_paths(volume)
        volume_path = Path(v["Location"])
        files = []
        for content in volume.findall("Content"):
            for file in content.findall("File"):
                d = file.attrib
                d["fullpath"] = volume_path / d["Name"]
                files.append(d)
            for folder in content.findall("Folder"):
                folder_path = volume_path / folder.attrib["Name"]
                files += self._get_folder_files(folder, folder_path)
        v["files"] = files
        return v

    def _scan_volumes(self, fileindex: ElementTree.Element) -> List[Dict]:
        """Get paths and file lists for all volumes"""
        return [self._scan_volume(volume) for volume in fileindex.findall("Volume")]

    def _check_all_files_present(self) -> None:
        in_fileindex = set([f["Content-Id"] for f in self.files_in_fileindex])
        in_archive = set(self.files_in_archive)
        not_in_archive = in_fileindex - in_archive
        not_in_fileindex = in_archive - in_fileindex
        if len(not_in_archive) > 0:
            warnings.warn(
                f"{len(not_in_archive)} files were not found under Files/Content."
            )
        if len(not_in_fileindex) > 0:
            warnings.warn(
                f"{len(not_in_fileindex)} files were not found in the file system."
            )
        if len(not_in_archive) == len(not_in_fileindex) == 0:
            print(f"Files are complete.")

    def _list_files_in_archive(self) -> List[str]:
        with ZipFile(self.source, "r") as file:
            return [
                Path(f).name for f in file.namelist() if f.startswith("Files/Content/")
            ]

    def _list_files_in_fileindex(
        self, fill_content_id: bool = True
    ) -> List[Dict[str, str | Path]]:
        # get files listed in fileindex.xml
        files = [file for volume in self.volumes for file in volume["files"]]

        # add missing ids
        if fill_content_id is True:
            for file in files:
                if "Content-Id" not in file:
                    file["Content-Id"] = file["Name"]

        return files

    def get_name_path_map(self, key: str = "Content-Id") -> Dict[str, Path]:
        return {f[key]: f["fullpath"] for f in self.files_in_fileindex}

    def get_mod_times(self, key: str = "Content-Id") -> Dict[str, str]:
        return {f[key]: f["Modified"] for f in self.files_in_fileindex}

    @staticmethod
    def _set_modification_date(
        file: Path,
        modified: datetime | Tuple,
        accessed: datetime | Tuple = None,
    ) -> None:
        if isinstance(modified, tuple):
            modified = datetime(*modified)
        if isinstance(accessed, tuple):
            accessed = datetime(*accessed)
        elif accessed is None:
            accessed = datetime.now()
        os.utime(file, (accessed.timestamp(), modified.timestamp()))

    def _extract_file(
        self,
        zf: zipfile.ZipFile,
        source: str,
        destination: Path,
        keep_date_time: bool = True,
    ) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as f:
            f.write(zf.read(source))
        if keep_date_time is True:
            self._set_modification_date(
                file=destination, modified=zf.getinfo(source).date_time
            )

    def extract_files(
        self,
        destination: str | Path = default_destination,
        check_completeness: bool = True,
        dry_run: bool = False,
        verbose: bool = False,
        keep_modification_date: bool = True,
    ) -> None:

        if check_completeness:
            self._check_all_files_present()

        with ZipFile(self.source, "r") as zf:
            for cid, path in self.get_name_path_map().items():
                # remove root anchor to make relative path
                path = path.relative_to(path.root)
                if str(path)[0] == "\\":
                    path = Path(str(path)[1:])
                clean_path = destination / path
                # extract file
                if not dry_run:
                    self._extract_file(
                        zf=zf,
                        source=self.content_path + cid,
                        destination=clean_path,
                        keep_date_time=keep_modification_date,
                    )
                if verbose:
                    print(clean_path)
        print(f"Done.")


if __name__ == "__main__":
    dbks = DBKScanner(source_file)
    dbks.extract_files()
