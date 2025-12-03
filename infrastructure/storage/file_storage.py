
import os
import json
import shutil
from typing import List, Dict, Any, Optional

class FileStorage:
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def save_file(self, filename: str, content: Any, encoding: str = "utf-8") -> str:
        file_path = os.path.join(self.base_dir, filename)

        if isinstance(content, (dict, list)):
            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(content, f, indent=4, ensure_ascii=False)
        else:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(str(content))

        return file_path

    def load_file(self, filename: str, encoding: str = "utf-8") -> Any:
        file_path = os.path.join(self.base_dir, filename)

        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content

    def copy_file(self, source_path: str, target_filename: str) -> str:
        target_path = os.path.join(self.base_dir, target_filename)
        shutil.copy(source_path, target_path)
        return target_path

    def delete_file(self, filename: str) -> bool:
        file_path = os.path.join(self.base_dir, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return True

        return False

    def file_exists(self, filename: str) -> bool:
        file_path = os.path.join(self.base_dir, filename)
        return os.path.exists(file_path)

    def list_files(self, extension: Optional[str] = None) -> List[str]:
        files = []

        for filename in os.listdir(self.base_dir):
            if extension is None or filename.endswith(f".{extension}"):
                files.append(filename)

        return files

    def create_subdirectory(self, subdir_name: str) -> str:
        subdir_path = os.path.join(self.base_dir, subdir_name)

        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

        return subdir_path

    def get_file_path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)
