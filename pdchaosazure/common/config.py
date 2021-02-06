import io
import json
import os

from chaoslib.types import Configuration
from logzero import logger
from msrestazure import azure_cloud


def load_secrets():
    """Load secrets from experiments or azure credential file.

    :returns: a secret object

    Load secrets from multiple sources that can contain different format
    such as azure credential file or experiment secrets section.
    The latter takes precedence over azure credential file.

    Function returns following dictionary object:
    ```python
    {
        # always available
        "cloud": "variable contains msrest cloud object"

        # always available: authentication with service principal
        "client_id": "variable contains client id",
        "client_secret": "variable contains client secret",
        "tenant_id": "variable contains tenant id",

    }
    ```

    :Loading secrets from azure credential file:

    Function will try to load secrets from the
    azure credential file. Path to the file should
    be set under AZURE_AUTH_LOCATION environment variable.

    Function will try to load following secrets from azure credential file:
    ```json
    {
        "clientId": "AZURE_CLIENT_ID",
        "clientSecret": "AZURE_CLIENT_SECRET",
        "tenantId": "AZURE_TENANT_ID",
        "resourceManagerEndpointUrl": "AZURE_RESOURCE_MANAGER_ENDPOINT",
        ...
    }
    ```
    More info about azure credential file may be found:
    https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate

    """

    # lookup for credentials in azure auth file
    credentials = _load_credentials_from_auth_file()
    if credentials:
        rm_endpoint = credentials.get('resourceManagerEndpointUrl')
        return {
            'client_id': credentials.get('clientId'),
            'client_secret': credentials.get('clientSecret'),
            'tenant_id': credentials.get('tenantId'),
            # load cloud object
            'cloud': azure_cloud.get_cloud_from_metadata_endpoint(rm_endpoint),
            # access token is not supported for credential files
            'access_token': None,
        }

    # no secretes
    logger.warn("Unable to load Azure credentials.")
    return {}


def load_timeout(experiment_configuration: Configuration) -> int:
    """ Defaults to 600 seconds if no timeout is given. """
    result = 600

    if experiment_configuration:
        result = experiment_configuration.get("timeout", result)

    return result


def load_subscription_id() -> str:
    # lookup in Azure auth file
    credentials = _load_credentials_from_auth_file()
    if credentials:
        return credentials.get('subscriptionId')

    # no configuration
    logger.warn("Unable to load subscription id.")
    return None


def _load_credentials_from_auth_file():
    auth_path = os.environ.get('AZURE_AUTH_LOCATION')
    credential_file = {}
    if auth_path and os.path.exists(auth_path):
        with io.open(auth_path, 'r', encoding='utf-8-sig') as auth_fd:
            credential_file = json.load(auth_fd)
    return credential_file
