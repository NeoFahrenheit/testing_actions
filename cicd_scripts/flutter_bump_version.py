import argparse
import sys

from enum import Enum

class VersionType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    BUILD = "build"

class Version:
    def __init__(self):
        self.file_path = './pubspec.yaml'
        self.bump_type : VersionType | None
        self.file_lines = self._get_file_lines()
        self.index = self._get_version_line_index()
        self.current_version = self._get_current_version()
        self.next_version : str | None

    def set_bump_type(self, bump_type: str) -> None:

        if bump_type not in VersionType._value2member_map_:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        self.bump_type = VersionType(bump_type)

    def _get_file_lines(self) -> list[str]:

        with open(self.file_path, 'r') as f:
            return f.readlines()

    def _get_version_line_index(self) -> int:

        count = 0
        for line in self.file_lines:
            if line.startswith('version'):
                return count
            count += 1

        raise Exception(f"version not found in {self.file_path}.")

    def _get_current_version(self) -> str:

        return self.file_lines[self.index].split(':')[1].strip()

    def get_next_version(self) -> str:
        build_str = self.current_version.split("+")[1]
        major_str, minor_str, patch_str = self.current_version.split("+")[0].split(".")
        
        major = int(major_str)
        minor = int(minor_str)
        patch = int(patch_str)
        build = int(build_str)

        match self.bump_type:
            case VersionType.BUILD:
                build += 1
            case VersionType.PATCH:
                patch += 1
                build = 1
            case VersionType.MINOR:
                minor += 1
                patch = 0
                build = 1
            case VersionType.MAJOR:
                major += 1
                minor = 0
                patch = 0
                build = 1

        self.next_version = f"{major}.{minor}.{patch}+{build}"
        return self.next_version

    def write_new_version(self) -> None:

        with open(self.file_path, 'w') as f:
            self.file_lines[self.index] = f"version: {self.next_version}\n"
            f.writelines(self.file_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Bump version script")
    parser.add_argument("version_type", choices=["major", "minor", "patch", "build"], help="Type of version bump")
    args = parser.parse_args()
    version_type = args.version_type

    version_handler = Version()
    version_handler.set_bump_type(version_type)
    next_version = version_handler.get_next_version()
    version_handler.write_new_version()

    print(next_version)