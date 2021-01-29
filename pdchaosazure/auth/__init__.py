import contextlib
from typing import Dict
from urllib.parse import urlparse

from azure.identity import ClientSecretCredential
from chaoslib.exceptions import InterruptExecution


@contextlib.contextmanager
def auth(secrets: Dict) -> ClientSecretCredential:
    """
    Create Azure authentication client from a provided secrets.

    Service principle and token based auth types are supported. Token
    based auth do not currently support refresh token functionality.

    Type of authentication client is determined based on passed secrets.

    For example, secrets that contains a `client_id`, `client_secret` and
    `tenant_id` will create ServicePrincipalAuth client
    ```python
    {
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "tenant_id": "AZURE_TENANT_ID"
    }
    ```
    If you are not working with Public Global Azure, e.g. China Cloud
    you can provide `msrestazure.azure_cloud.Cloud` object. If omitted the
    Public Cloud is taken as default. Please refer to msrestazure.azure_cloud
    ```python
    {
        "client_id": "xxxxxxx",
        "client_secret": "*******",
        "tenant_id": "@@@@@@@@@@@",
        "cloud": "msrestazure.azure_cloud.Cloud"
    }
    ```

    Using this function goes as follows:

    ```python
    with auth(secrets) as cred:
        subscription_id = configuration.get("subscription_id")
        resource_client = ResourceManagementClient(cred, subscription_id)
        compute_client = ComputeManagementClient(cred, subscription_id)
    ```

    Again, if you are not working with Public Azure Cloud,
    and you set azure_cloud in secret,
    this will pass one more parameter `base_url` to above function.
    ```python
    with auth(secrets) as cred:
        cloud = cred.get('cloud')
        client = ComputeManagementClient(
            credentials=cred, subscription_id=subscription_id,
                        base_url=cloud.endpoints.resource_manager)
    ```

    """

    try:
        credential = ClientSecretCredential(
            tenant_id=secrets.get('tenant_id'),
            client_id=secrets.get('client_id'),
            client_secret=secrets.get('client_secret'),
            authority=urlparse(secrets.get('cloud').endpoints.active_directory).hostname
        )
    except ValueError as e:
        raise InterruptExecution(str(e))
    yield credential
