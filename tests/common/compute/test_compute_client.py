from unittest.mock import patch, MagicMock

from pdchaosazure.common.compute import client
from tests.data import secrets_provider


@patch('pdchaosazure.common.config._load_credentials_from_auth_file', autospec=True)
@patch('pdchaosazure.common.compute.client.auth', autospec=True)
def test_init(auth, load):
    load.return_value = secrets_provider.auth_file()
    creds = MagicMock()
    auth.return_value = creds

    clnt = client.init()

    assert clnt
    assert clnt._config.subscription_id == "AZURE_SUBSCRIPTION_ID"
