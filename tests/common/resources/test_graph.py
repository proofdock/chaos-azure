from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from pdchaosazure.common.resources.graph import fetch_resources
from tests.data import config_provider, secrets_provider, graph_provider


@patch('pdchaosazure.common.resources.graph.init_client', autospec=True)
def test_happily_fetch_resources(mocked_graph_client):
    secrets = secrets_provider.provide_secrets_germany()
    config = config_provider.provide_default_config()

    mocked_graph_client.return_value.resources.return_value.data = graph_provider.default()
    mocked_graph_client.return_value.api_version = '2019-04-01'

    resources = fetch_resources("", "Microsoft.Compute/virtualMachines", secrets, config)

    assert resources[0]['name'] == 'vmachine1'


@patch('pdchaosazure.common.resources.graph.init_client', autospec=True)
def test_sadly_fetch_empty_resources(mocked_graph_client):
    secrets = secrets_provider.provide_secrets_germany()
    config = config_provider.provide_default_config()

    mocked_graph_client.return_value.resources.return_value.data = graph_provider.empty()
    mocked_graph_client.return_value.api_version = '2019-04-01'

    with pytest.raises(FailedActivity):
        fetch_resources("", "Microsoft.Compute/virtualMachines", secrets, config)
