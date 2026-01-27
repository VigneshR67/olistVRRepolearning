import zipfile
from pathlib import Path
from typing import List


class UnzipReader:
    """
    Handles extraction of zip files before ingestion.
    """

    def extract(
        self,
        zip_path: str,
        extract_dir: str,
        overwrite: bool = True
    ) -> List[str]:
        """
        Extracts zip file contents to extract_dir.

        Returns list of extracted file paths.
        """

        zip_path = Path(zip_path)
        extract_dir = Path(extract_dir)

        if overwrite and extract_dir.exists():
            for f in extract_dir.iterdir():
                if f.is_file():
                    f.unlink()

        extract_dir.mkdir(parents=True, exist_ok=True)

        extracted_files = []

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
            extracted_files = [
                str(extract_dir / name)
                for name in zip_ref.namelist()
                if not name.endswith("/")
            ]

        return extracted_files
