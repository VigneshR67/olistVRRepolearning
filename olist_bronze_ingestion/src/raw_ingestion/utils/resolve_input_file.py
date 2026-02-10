from pathlib import Path
import zipfile
from typing import List


def resolve_input_files(volume_path: str) -> List[str]:
    """
    Resolves input files from a Unity Catalog Volume path.
    - If ZIP files exist → extract in same folder
    - Returns list of CSV file paths to ingest
    """

    base_path = Path(volume_path)

    if not base_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {volume_path}")

    files_to_ingest: list[str] = []
    seen_filenames: set[str] = set()

    for item in base_path.iterdir():

        # Case 1: ZIP file
        if item.is_file() and item.suffix.lower() == ".zip":

            with zipfile.ZipFile(item, "r") as zip_ref:
                zip_ref.extractall(base_path)

                for name in zip_ref.namelist():
                    if name.endswith(".csv"):
                        csv_path = base_path / name
                        filename = csv_path.name

                        if filename not in seen_filenames:
                            files_to_ingest.append(str(csv_path))
                            seen_filenames.add(filename)

        # Case 2: CSV file
        elif item.is_file() and item.suffix.lower() == ".csv":
            filename = item.name

            if filename not in seen_filenames:
                files_to_ingest.append(str(item))
                seen_filenames.add(filename)

    if not files_to_ingest:
        raise ValueError("No CSV files found for ingestion")

    return files_to_ingest
