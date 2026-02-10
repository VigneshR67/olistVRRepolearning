#should be reading from databricks secret scope
import re


def extract_storage_account(adls_path: str) -> str:
    """
    Extract storage account name from ABFSS path.
    """

    pattern = r"abfss://.*@(.*?)\.dfs\.core\.windows\.net"
    match = re.search(pattern, adls_path)

    if not match:
        raise ValueError(f"Invalid ADLS path: {adls_path}")

    return match.group(1)
