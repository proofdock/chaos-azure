from unittest.mock import patch

from pdchaosazure.webapp.constants import RES_TYPE_WEBAPP
from pdchaosazure.webapp.probes import count_webapps, describe_webapps

CONFIG = {
    "azure": {
        "subscription_id": "X"
    }
}

SECRETS = {
    "client_id": "X",
    "client_secret": "X",
    "tenant_id": "X"
}

resource = {
    'name': 'chaos-webapp',
    'resourceGroup': 'rg'}


@patch('pdchaosazure.webapp.probes.fetch_resources', autospec=True)
def test_count_webapp(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    count = count_webapps(f, CONFIG, SECRETS)

    assert count == 1
    fetch.assert_called_with(f, RES_TYPE_WEBAPP, SECRETS, CONFIG)


@patch('pdchaosazure.webapp.probes.fetch_resources', autospec=True)
def test_describe_webapp(fetch):
    resource_list = [resource]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    result = describe_webapps(f, CONFIG, SECRETS)

    assert result == resource_list
    fetch.assert_called_with(f, RES_TYPE_WEBAPP, SECRETS, CONFIG)
