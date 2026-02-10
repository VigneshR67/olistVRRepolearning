from raw_ingestion.utils.path_utils import extract_storage_account


_configured_accounts = set()


def authenticate_adls(
    spark,
    adls_path: str,
    tenant_id: str,
    client_id: str,
    client_secret: str
) -> None:
    """
    Authenticate ADLS storage account dynamically using Service Principal.
    """

    storage_account = extract_storage_account(adls_path)

    if storage_account in _configured_accounts:
        return

    configs = {
        f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net": "OAuth",

        f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net":
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",

        f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net":
            client_id,

        f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net":
            client_secret,

        f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net":
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    }

    for key, value in configs.items():
        spark.conf.set(key, value)

    _configured_accounts.add(storage_account)
