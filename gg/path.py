import os
import pathlib


class Path:
    @staticmethod
    def get_root_path() -> str:
        current_path = pathlib.Path(os.getcwd())
        while current_path:
            if ".gg" in os.listdir(current_path):
                return current_path.as_posix()
            elif current_path.as_posix() == "/":
                break
            else:
                current_path = current_path.parent

        return os.getcwd()
